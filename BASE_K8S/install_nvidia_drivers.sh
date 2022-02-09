#!/bin/bash -e

# Install NVIDIA drivers, including X graphic drivers by omitting --x-{prefix,module-path,library-path,sysconfig-path}
if ! command -v nvidia-xconfig &> /dev/null; then
  export DRIVER_VERSION=$(head -n1 </proc/driver/nvidia/version | awk '{print $8}')
  cd /tmp
  # remove any remnants which could be there from before...
  rm -fr /tmp/NVIDIA-Linux-x86_64-470.82.01 /tmp/NVIDIA-Linux-x86_64-470.82.01.run
  if [ ! -f "/tmp/NVIDIA-Linux-x86_64-$DRIVER_VERSION.run" ]; then
    curl -fsL -O "https://us.download.nvidia.com/XFree86/Linux-x86_64/$DRIVER_VERSION/NVIDIA-Linux-x86_64-$DRIVER_VERSION.run" || curl -fsL -O "https://us.download.nvidia.com/tesla/$DRIVER_VERSION/NVIDIA-Linux-x86_64-$DRIVER_VERSION.run" || { echo "Failed NVIDIA GPU driver download. Exiting."; exit 1; }
  fi
  sudo sh "NVIDIA-Linux-x86_64-$DRIVER_VERSION.run" -x
  cd "NVIDIA-Linux-x86_64-$DRIVER_VERSION"
  sudo ./nvidia-installer --silent \
                    --no-kernel-module \
                    --install-compat32-libs \
                    --no-nouveau-check \
                    --no-nvidia-modprobe \
                    --no-rpms \
                    --no-backup \
                    --no-check-for-alternate-installs \
                    --no-libglx-indirect \
                    --no-install-libglvnd
  sudo rm -rf /tmp/NVIDIA* && cd ~
fi
