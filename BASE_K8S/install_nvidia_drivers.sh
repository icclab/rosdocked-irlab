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
# The RAP nodes are not homogeneous (some run 555.42.02 / CUDA 12.5, at least one
# runs a 13.x driver), so a pod landing on a node whose driver differs from the
# baked one installs at start. To stop that re-downloading ~400 MB per pod, mount
# a per-node cache directory at $NVIDIA_DRIVER_CACHE_DIR, e.g.:
#
#   volumes:
#     - name: nvidia-driver-cache
#       hostPath: { path: /opt/nvidia-driver-cache, type: DirectoryOrCreate }
#   volumeMounts:
#     - { name: nvidia-driver-cache, mountPath: /var/cache/nvidia-driver }
#
# The first pod on a node populates it; every later pod installs from disk.
#
# Must run as root (build and entrypoint both invoke it via sudo).
################################################################################

STAMP=/etc/nvidia-userspace-driver-version
CACHE_DIR=${NVIDIA_DRIVER_CACHE_DIR:-/var/cache/nvidia-driver}

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

RUN_FILE="NVIDIA-Linux-x86_64-$DRIVER_VERSION.run"

# Only use the cache when it already exists and is writable, i.e. when a volume
# is actually mounted there. Deliberately no mkdir: at build time the directory
# is absent, so the installer goes to /tmp and gets deleted afterwards instead of
# leaving ~400 MB of .run file in the image.
if [ -d "$CACHE_DIR" ] && [ -w "$CACHE_DIR" ]; then
  WORK_DIR=$CACHE_DIR
else
  WORK_DIR=/tmp
fi

# `--check` verifies the self-extractor's embedded checksum, so a half-written
# file left behind by an evicted pod is re-downloaded instead of used.
if [ -s "$WORK_DIR/$RUN_FILE" ] && sh "$WORK_DIR/$RUN_FILE" --check >/dev/null 2>&1; then
  echo "install_nvidia_drivers: using cached $WORK_DIR/$RUN_FILE"
else
  rm -f "$WORK_DIR/$RUN_FILE"
  # Note the URL order: the tesla/ path 404s for some versions (555.42.02), while
  # XFree86/ carries both the desktop and datacenter releases.
  ( cd "$WORK_DIR" && \
    curl -fsL -O "https://us.download.nvidia.com/XFree86/Linux-x86_64/$DRIVER_VERSION/$RUN_FILE" \
    || curl -fsL -O "https://us.download.nvidia.com/tesla/$DRIVER_VERSION/$RUN_FILE" ) \
  || { echo "Failed NVIDIA GPU driver download for $DRIVER_VERSION. Exiting." >&2; exit 1; }
fi

# Extract into /tmp, never into the (possibly shared, possibly read-only) cache.
cd /tmp
rm -rf "/tmp/NVIDIA-Linux-x86_64-$DRIVER_VERSION"
sh "$WORK_DIR/$RUN_FILE" -x
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
rm -rf "/tmp/NVIDIA-Linux-x86_64-$DRIVER_VERSION"
# Keep the installer only when it lives in a mounted cache; never in the image.
# (Plain `[ ... ] && rm` would abort the script under `set -e` when false.)
if [ "$WORK_DIR" = "/tmp" ]; then
  rm -f "/tmp/$RUN_FILE"
fi

echo "$DRIVER_VERSION" > "$STAMP"
echo "install_nvidia_drivers: done ($DRIVER_VERSION)."
