#!/usr/bin/env bash
################################################################################
# Decide whether "option A" (drop Xorg-on-GPU, render via EGL) can work for our
# stack, in about 15 minutes, without converting anything.
#
# Why: Xorg inside the container needs nvidia_drv.so + libglxserver_nvidia.so,
# which nvidia-container-toolkit does not inject, so the driver must be baked in
# and pinned to the node's version. If GL works with NO Xorg at all, that pin --
# and the whole runtime driver-install dance -- goes away, and one image runs on
# every node regardless of its driver.
#
# Run it in a THROWAWAY container on a GPU node, with the normal entrypoint
# overridden so that no Xorg is started:
#
#   docker run --rm -it --gpus all -e NVIDIA_DRIVER_CAPABILITIES=all \
#     --entrypoint bash robopaas/rosdocked-jazzy-k8s:cuda12.5.0 \
#     -c "$(cat test/probe_egl_rendering.sh)"
#
# or on the cluster:
#   kubectl run egl-probe --rm -it --restart=Never --image=robopaas/rosdocked-jazzy-k8s:cuda12.5.0 \
#     --overrides='{"spec":{"containers":[{"name":"egl-probe","image":"robopaas/rosdocked-jazzy-k8s:cuda12.5.0","command":["bash","-lc","..."],"resources":{"limits":{"nvidia.com/gpu":1}}}]}}'
#
# Read the PASS/FAIL summary at the end. If the VirtualGL/rviz2 line fails, stop:
# keep the current Xorg + runtime driver-match setup and do not convert.
################################################################################
set -u
VGL_VERSION=3.1.5
RESULTS=()
note() { echo; echo "=== $* ==="; }
record() { RESULTS+=("$1|$2"); }

note "0. Environment"
echo "host driver: $(awk '{print $8; exit}' /proc/driver/nvidia/version 2>/dev/null || echo UNKNOWN)"
nvidia-smi --query-gpu=name,driver_version --format=csv,noheader 2>&1 | head -3
for f in /usr/lib/xorg/modules/drivers/nvidia_drv.so \
         /usr/lib/x86_64-linux-gnu/libEGL_nvidia.so.0 \
         /usr/lib/x86_64-linux-gnu/libGLX_nvidia.so.0; do
  [ -e "$f" ] && echo "present: $f" || echo "ABSENT:  $f"
done
pgrep -x Xorg >/dev/null && echo "WARNING: an Xorg is already running -- this probe must run with no Xorg." || echo "good: no Xorg running"

note "1. Does the GPU expose an EGL device with no X server at all?"
# eglinfo comes from mesa-utils-extra, already in the image.
if eglinfo -B 2>/dev/null | grep -iq "device platform" || eglinfo 2>/dev/null | grep -iq nvidia; then
  eglinfo -B 2>/dev/null | sed -n '1,25p'
  record "EGL device visible without X" PASS
else
  echo "eglinfo found no NVIDIA EGL device."
  record "EGL device visible without X" FAIL
fi

note "2. Gazebo server rendering over EGL, no X (the GPU-heavy path)"
# --headless-rendering makes gz-rendering use EGL directly; no VirtualGL involved.
unset DISPLAY
timeout 60 gz sim -s -r -v 3 --headless-rendering shapes.sdf >/tmp/gz.log 2>&1
if grep -Eqi "ogre|egl|render" /tmp/gz.log && ! grep -Eqi "failed to (create|initial)|unable to create.*(context|render)|llvmpipe" /tmp/gz.log; then
  record "gz sim --headless-rendering (EGL, no X)" PASS
else
  echo "--- tail of /tmp/gz.log ---"; tail -20 /tmp/gz.log
  record "gz sim --headless-rendering (EGL, no X)" FAIL
fi

note "3. Install Xvfb + VirtualGL (this is the part option A depends on)"
sudo apt-get update -qq && sudo apt-get install -y -qq xvfb x11-apps >/dev/null 2>&1
curl -fsSLO "https://github.com/VirtualGL/virtualgl/releases/download/${VGL_VERSION}/virtualgl_${VGL_VERSION}_amd64.deb" \
  && sudo apt-get install -y -qq "./virtualgl_${VGL_VERSION}_amd64.deb" >/dev/null 2>&1 \
  && record "VirtualGL ${VGL_VERSION} installs" PASS \
  || { record "VirtualGL ${VGL_VERSION} installs" FAIL; }

note "4. GL renderer under Xvfb + VirtualGL EGL back end"
Xvfb :1 -screen 0 1920x1080x24 >/tmp/xvfb.log 2>&1 &
sleep 3
export DISPLAY=:1
echo "-- without VirtualGL (expect llvmpipe: that is the point) --"
glxinfo -B 2>/dev/null | sed -n 's/^OpenGL renderer string: /  renderer: /p'
echo "-- with VirtualGL EGL back end --"
VGL_RENDERER=$(vglrun -d egl0 glxinfo -B 2>/tmp/vgl.log | sed -n 's/^OpenGL renderer string: //p')
echo "  renderer: ${VGL_RENDERER:-<none>}"
case "$VGL_RENDERER" in
  *NVIDIA*|*A30*) record "vglrun -d egl0 gives GPU renderer" PASS ;;
  *)              tail -10 /tmp/vgl.log; record "vglrun -d egl0 gives GPU renderer" FAIL ;;
esac

note "5. rviz2 under VirtualGL EGL (the risky client)"
# rviz2 is Ogre 1.12 + Qt, the most likely thing to trip on a missing GLX
# extension. Survive 25 s, and prove it actually drew something.
source /opt/ros/"${ROS_DISTRO:-jazzy}"/setup.bash
vglrun -d egl0 rviz2 >/tmp/rviz.log 2>&1 &
RVIZ_PID=$!
sleep 25
if kill -0 "$RVIZ_PID" 2>/dev/null; then
  xwd -root -display :1 > /tmp/rviz.xwd 2>/dev/null
  SIZE=$(stat -c%s /tmp/rviz.xwd 2>/dev/null || echo 0)
  # A blank Xvfb root window compresses to almost nothing; a drawn rviz does not.
  UNIQ=$(xwd -root -display :1 2>/dev/null | gzip -1 | wc -c)
  echo "screenshot: ${SIZE} bytes raw, ${UNIQ} bytes gzipped (blank screen gzips very small)"
  grep -Ei "opengl|ogre|glx|egl|error" /tmp/rviz.log | head -10
  if [ "$UNIQ" -gt 20000 ]; then record "rviz2 renders under VirtualGL EGL" PASS
  else record "rviz2 renders under VirtualGL EGL (screen looks blank)" FAIL; fi
  kill "$RVIZ_PID" 2>/dev/null
else
  echo "--- tail of /tmp/rviz.log ---"; tail -25 /tmp/rviz.log
  record "rviz2 renders under VirtualGL EGL (crashed)" FAIL
fi

note "SUMMARY"
for r in "${RESULTS[@]}"; do printf '  %-52s %s\n' "${r%%|*}" "${r##*|}"; done
echo
echo "Decision rule:"
echo "  * all PASS            -> option A is viable; converting is mechanical."
echo "  * only step 2 passes  -> run the Gazebo server headless over EGL, but keep"
echo "                           Xorg + the runtime driver match for the desktop."
echo "  * step 4 or 5 fails   -> STOP. Keep the current setup. Not worth the debugging."
echo
echo "Also worth eyeballing over VNC before trusting it, if the above passes:"
echo "  vglrun -d egl0 ros2 launch icclab_summit_xl summit_xl_simulation.launch.py"
