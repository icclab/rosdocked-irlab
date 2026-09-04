#!/bin/bash -e

trap "echo TRAPed signal" HUP INT QUIT KILL TERM

echo "ros:$PASSWD" | sudo chpasswd
sudo rm -rf /tmp/.X*
sudo ln -snf "/usr/share/zoneinfo/$TZ" /etc/localtime && echo "$TZ" | sudo tee /etc/timezone > /dev/null

sudo ln -snf /dev/ptmx /dev/tty7
sudo /etc/init.d/dbus start
# source /opt/gstreamer/gst-env

# Make sure the userspace driver in the image matches the host kernel module.
# They must agree exactly or GLX breaks; a cluster driver upgrade would otherwise
# silently leave every pod on software rendering. install_nvidia_drivers.sh is a
# no-op when the baked version already matches, so this normally costs nothing.
if [ -r /proc/driver/nvidia/version ]; then
  HOST_DRIVER=$(awk '{print $8; exit}' /proc/driver/nvidia/version)
  IMAGE_DRIVER=$(cat /etc/nvidia-userspace-driver-version 2>/dev/null || true)
  if [ "$HOST_DRIVER" != "$IMAGE_DRIVER" ]; then
    echo "NVIDIA userspace driver in image: '${IMAGE_DRIVER:-none}', host: '$HOST_DRIVER' -- installing match."
    # Non-fatal: a node without egress to us.download.nvidia.com should not put
    # the pod in a crash loop. The renderer check below reports the consequence.
    sudo /opt/install_nvidia_drivers.sh "$HOST_DRIVER" \
      || echo "WARNING: driver install failed -- expect software rendering." >&2
  fi
else
  echo "WARNING: /proc/driver/nvidia/version not readable -- no GPU visible to this container?" >&2
fi

if grep -Fxq "allowed_users=console" /etc/X11/Xwrapper.config; then
  sudo sed -i "s/allowed_users=console/allowed_users=anybody/;$ a needs_root_rights=yes" /etc/X11/Xwrapper.config
fi

if [ -f "/etc/X11/xorg.conf" ]; then
  sudo rm "/etc/X11/xorg.conf"
fi

if [ "$NVIDIA_VISIBLE_DEVICES" == "all" ]; then
  export GPU_SELECT=$(sudo nvidia-smi --query-gpu=uuid --format=csv | sed -n 2p)
elif [ -z "$NVIDIA_VISIBLE_DEVICES" ]; then
  export GPU_SELECT=$(sudo nvidia-smi --query-gpu=uuid --format=csv | sed -n 2p)
else
  export GPU_SELECT=$(sudo nvidia-smi --id=$(echo "$NVIDIA_VISIBLE_DEVICES" | cut -d ',' -f1) --query-gpu=uuid --format=csv | sed -n 2p)
  if [ -z "$GPU_SELECT" ]; then
    export GPU_SELECT=$(sudo nvidia-smi --query-gpu=uuid --format=csv | sed -n 2p)
  fi
fi

if [ -z "$GPU_SELECT" ]; then
  echo "No NVIDIA GPUs detected. Exiting."
  exit 1
fi

HEX_ID=$(sudo nvidia-smi --query-gpu=pci.bus_id --id="$GPU_SELECT" --format=csv | sed -n 2p)
IFS=":." ARR_ID=($HEX_ID)
unset IFS
BUS_ID=PCI:$((16#${ARR_ID[1]})):$((16#${ARR_ID[2]})):$((16#${ARR_ID[3]}))
export MODELINE=$(cvt -r "${SIZEW}" "${SIZEH}" "${REFRESH}" | sed -n 2p)
sudo nvidia-xconfig --virtual="${SIZEW}x${SIZEH}" --depth="$CDEPTH" --mode=$(echo "$MODELINE" | awk '{print $2}' | tr -d '"') --allow-empty-initial-configuration --no-probe-all-gpus --busid="$BUS_ID" --only-one-x-screen --connected-monitor="$VIDEO_PORT"
sudo sed -i '/Driver\s\+"nvidia"/a\    Option         "ModeValidation" "NoMaxPClkCheck, NoEdidMaxPClkCheck, NoMaxSizeCheck, NoHorizSyncCheck, NoVertRefreshCheck, NoVirtualSizeCheck, NoExtendedGpuCapabilitiesCheck, NoTotalSizeCheck, NoDualLinkDVICheck, NoDisplayPortBandwidthCheck, AllowNon3DVisionModes, AllowNonHDMI3DModes, AllowNonEdidModes, NoEdidHDMI2Check, AllowDpInterlaced"' /etc/X11/xorg.conf
sudo sed -i '/Section\s\+"Monitor"/a\    '"$MODELINE" /etc/X11/xorg.conf
sudo sed -i 's/Option         "DPMS"/Option         "DPMS" "false"/g' /etc/X11/xorg.conf

export DISPLAY=":0"
export __GL_SYNC_TO_VBLANK="0"
Xorg vt7 -novtswitch -sharevts -dpi "${DPI}" +extension "MIT-SHM" "${DISPLAY}" &

# Wait for X11 to start
echo "Waiting for X socket"
until [ -S "/tmp/.X11-unix/X${DISPLAY/:/}" ]; do sleep 1; done
echo "X socket is ready"

# Fail loudly rather than silently rendering in software: llvmpipe here means the
# driver/X setup is broken, and Gazebo and rviz will crawl.
GL_RENDERER=$(DISPLAY="${DISPLAY}" glxinfo -B 2>/dev/null | sed -n 's/^OpenGL renderer string: //p')
case "$GL_RENDERER" in
  "")                     echo "WARNING: could not query OpenGL renderer -- GL may be broken." >&2 ;;
  *llvmpipe*|*softpipe*|*swrast*)
    echo "WARNING: SOFTWARE RENDERING ACTIVE (renderer: $GL_RENDERER)." >&2
    echo "         The GPU is not being used. Check the driver version match above and Xorg.0.log." >&2 ;;
  *)                      echo "GPU rendering active: $GL_RENDERER" ;;
esac

# start noVNC
sudo x11vnc -display "${DISPLAY}" -passwd "${BASIC_AUTH_PASSWORD:-$PASSWD}" -shared -forever -repeat -xkb -xrandr "resize" -rfbport 5900 &
/opt/noVNC/utils/novnc_proxy --vnc localhost:5900 --listen 8080 --heartbeat 10 &

# Add custom processes below this section or within `supervisord.conf`
xfce4-session &

echo "Session Running. Press [Return] to exit."
read
