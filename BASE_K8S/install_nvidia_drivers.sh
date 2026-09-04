#!/bin/bash -e
################################################################################
# Install the NVIDIA *userspace* driver (no kernel module) at a given version.
#
# Why this exists at all: we run a real Xorg on the GPU inside the container,
# which needs nvidia_drv.so and libglxserver_nvidia.so. nvidia-container-toolkit
# deliberately does NOT inject those (they appear in none of the capability
# arrays in libnvidia-container's src/nvc_info.c), so the driver has to live in
# the image -- and its version must match the host kernel module EXACTLY or GLX
# fails and everything silently falls back to llvmpipe.
#
# Hence this script is called twice:
#   * at build time, with an explicit version (fast path, baked into the image)
#   * at container start, by entrypoint.sh, if the host driver differs from what
#     was baked -- which is what makes the image survive cluster driver upgrades
#
# Usage: install_nvidia_drivers.sh [DRIVER_VERSION]
#        With no argument, the host's running driver version is used.
#        With no argument and no host driver visible (e.g. a GPU-less build
#        machine), it is a no-op: the install then happens on first start.
#
# Must run as root (build and entrypoint both invoke it via sudo).
################################################################################

STAMP=/etc/nvidia-userspace-driver-version

DRIVER_VERSION="$1"
if [ -z "$DRIVER_VERSION" ] && [ -r /proc/driver/nvidia/version ]; then
  DRIVER_VERSION=$(awk '{print $8; exit}' /proc/driver/nvidia/version)
fi

if [ -z "$DRIVER_VERSION" ]; then
  echo "install_nvidia_drivers: no version given and no host driver visible;" \
       "skipping (entrypoint.sh will install the matching driver at start)."
  exit 0
fi

if [ "$(cat "$STAMP" 2>/dev/null)" = "$DRIVER_VERSION" ]; then
  echo "install_nvidia_drivers: userspace driver $DRIVER_VERSION already installed."
  exit 0
fi

echo "install_nvidia_drivers: installing NVIDIA userspace driver $DRIVER_VERSION"
cd /tmp
# Remove any remnants of an earlier attempt / a previously baked version.
rm -rf "/tmp/NVIDIA-Linux-x86_64-$DRIVER_VERSION" "/tmp/NVIDIA-Linux-x86_64-$DRIVER_VERSION.run"
curl -fsL -O "https://us.download.nvidia.com/XFree86/Linux-x86_64/$DRIVER_VERSION/NVIDIA-Linux-x86_64-$DRIVER_VERSION.run" \
  || curl -fsL -O "https://us.download.nvidia.com/tesla/$DRIVER_VERSION/NVIDIA-Linux-x86_64-$DRIVER_VERSION.run" \
  || { echo "Failed NVIDIA GPU driver download for $DRIVER_VERSION. Exiting." >&2; exit 1; }

sh "NVIDIA-Linux-x86_64-$DRIVER_VERSION.run" -x
cd "NVIDIA-Linux-x86_64-$DRIVER_VERSION"
./nvidia-installer --silent \
                  --no-kernel-module \
                  --install-compat32-libs \
                  --no-nouveau-check \
                  --no-nvidia-modprobe \
                  --no-rpms \
                  --no-backup \
                  --no-check-for-alternate-installs \
                  --no-libglx-indirect \
                  --no-install-libglvnd

# Scoped cleanup: the old version of this script did `rm -rf /tmp/*`, which at
# container start would also delete the X11 sockets in /tmp/.X11-unix.
cd /
rm -rf "/tmp/NVIDIA-Linux-x86_64-$DRIVER_VERSION" "/tmp/NVIDIA-Linux-x86_64-$DRIVER_VERSION.run"

echo "$DRIVER_VERSION" > "$STAMP"
echo "install_nvidia_drivers: done ($DRIVER_VERSION)."
