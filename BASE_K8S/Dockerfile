################################################################################
# ZHAW INIT
# Description:  Dockerfile to create the Base CPU Docker image
# Authors:      Leonardo Militano, Mark Straub, Giovanni Toffetti
# Date:         2022-05-04
################################################################################

# Base image
#FROM ghcr.io/ehfd/nvidia-glx-desktop:latest
ARG UBUNTU_RELEASE=20.04
FROM nvcr.io/nvidia/cudagl:11.4.2-runtime-ubuntu${UBUNTU_RELEASE}

################################################################################

# Arguments
ENV ROS_DISTRO=foxy
ENV DEBIAN_FRONTEND=noninteractive
ENV USER=ros

ARG UBUNTU_RELEASE
# Make all NVIDIA GPUs visible, but we want to manually install drivers
ARG NVIDIA_VISIBLE_DEVICES=all
# Supress interactive menu while installing keyboard-configuration
ENV NVIDIA_DRIVER_CAPABILITIES all
ENV PULSE_SERVER 127.0.0.1:4713

# Default environment variables (password is "mypasswd")
ENV TZ UTC
ENV SIZEW 1920
ENV SIZEH 1080
ENV REFRESH 60
ENV DPI 96
ENV CDEPTH 24
ENV VIDEO_PORT DFP
ENV PASSWD mypasswd
ENV NOVNC_ENABLE false
ENV WEBRTC_ENCODER nvh264enc
ENV WEBRTC_ENABLE_RESIZE false
ENV ENABLE_AUDIO true
ENV ENABLE_BASIC_AUTH true

################################################################################

# Fix of wrong key
# https://github.com/NVIDIA/nvidia-docker/issues/1631
RUN rm /etc/apt/sources.list.d/cuda.list
RUN apt-key del 7fa2af80
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils wget
RUN wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/cuda-keyring_1.0-1_all.deb
RUN dpkg -i cuda-keyring_1.0-1_all.deb

################################################################################

# Update apt sources using mirror
RUN sed -i -e 's/archive.ubuntu.com/mirror.cloudlab.zhaw.ch/g' /etc/apt/sources.list

# Install locales to prevent errors
RUN apt-get clean && \
    apt-get update && apt-get install --no-install-recommends -y locales && \
    rm -rf /var/lib/apt/lists/* && \
    locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# Install Xorg, MATE Desktop, and others
RUN dpkg --add-architecture i386 && \
    apt-get update && apt-get install --no-install-recommends -y \
        software-properties-common \
        build-essential \
        ca-certificates \
        kmod \
        libc6:i386 \
        libc6-dev \
        curl \
        file \
        gzip \
        zip \
        unzip \
        gcc \
        git \
        jq \
        make \
        python \
        python-numpy \
        python3 \
        python3-numpy \
        mlocate \
        nano \
        vim \
        htop \
        firefox \
        supervisor \
        net-tools \
        libpci3 \
        libelf-dev \
        libglvnd-dev \
        pkg-config \
        mesa-utils \
        mesa-utils-extra \
        libglu1 \
        libglu1:i386 \
        libsm6 \
        libxv1 \
        libxv1:i386 \
        libxtst6 \
        libxtst6:i386 \
        x11-xkb-utils \
        x11-xserver-utils \
        x11-apps \
        dbus-x11 \
        libdbus-c++-1-0v5 \
        xauth \
        xinit \
        xfonts-base \
        xkb-data \
        libxrandr-dev \
        xorg-dev && \
    apt-get install -y ubuntu-mate-desktop && \
    if [ "${UBUNTU_RELEASE}" = "18.04" ]; then apt-get install --no-install-recommends -y vulkan-utils; else apt-get install --no-install-recommends -y vulkan-tools; fi && \
    # Remove Bluetooth packages that throw errors
    apt-get autoremove --purge -y \
        blueman \
        pulseaudio-module-bluetooth && \
    rm -rf /var/lib/apt/lists/*

# # Install Google Chrome
# RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add - && \
#     bash -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list' && \
#     apt-get update && apt-get install google-chrome-stable

# Install Mircosoft Edge
RUN curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg && \
    install -o root -g root -m 644 microsoft.gpg /etc/apt/trusted.gpg.d/ && \
    sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/repos/edge stable main" > /etc/apt/sources.list.d/microsoft-edge-dev.list' && \
    rm microsoft.gpg && \
    apt update && apt install microsoft-edge-stable

# Install latest noVNC web interface for fallback
RUN apt-get update && apt-get install --no-install-recommends -y \
        autoconf \
        automake \
        autotools-dev \
        chrpath \
        debhelper \
        jq \
        python \
        python-numpy \
        python3 \
        python3-numpy \
        libc6-dev \
        libcairo2-dev \
        libjpeg-turbo8-dev \
        libssl-dev \
        libv4l-dev \
        libvncserver-dev \
        libtool-bin \
        libxdamage-dev \
        libxinerama-dev \
        libxrandr-dev \
        libxss-dev \
        libxtst-dev \
        libavahi-client-dev && \
    rm -rf /var/lib/apt/lists/* && \
    git clone https://github.com/LibVNC/x11vnc.git /tmp/x11vnc && \
    cd /tmp/x11vnc && autoreconf -fi && ./configure && make install && cd / && rm -rf /tmp/* && \
    NOVNC_VERSION=$(curl -fsSL "https://api.github.com/repos/noVNC/noVNC/releases/latest" | jq -r '.tag_name' | sed 's/[^0-9\.\-]*//g') && \
    curl -fsSL https://github.com/novnc/noVNC/archive/v${NOVNC_VERSION}.tar.gz | tar -xzf - -C /opt && \
    mv /opt/noVNC-${NOVNC_VERSION} /opt/noVNC && \
    ln -s /opt/noVNC/vnc.html /opt/noVNC/index.html && \
    git clone https://github.com/novnc/websockify /opt/noVNC/utils/websockify

# Add custom packages below this comment

# Create user with password ${PASSWD}
RUN apt-get update && apt-get install --no-install-recommends -y \
        sudo && \
    rm -rf /var/lib/apt/lists/* && \
    groupadd -g 1000 ${USER} && \
    useradd -ms /bin/bash ${USER} -u 1000 -g 1000 && \
    usermod -a -G adm,audio,cdrom,dialout,dip,fax,floppy,input,lp,lpadmin,netdev,plugdev,scanner,ssh,sudo,tape,tty,video,voice ${USER} && \
    echo "${USER} ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers && \
    chown ${USER}:${USER} /home/${USER} && \
    echo "${USER}:${PASSWD}" | chpasswd && \
    ln -snf "/usr/share/zoneinfo/$TZ" /etc/localtime && echo "$TZ" > /etc/timezone


################################################################################

# https://docs.ros.org/en/foxy/Installation/Ubuntu-Install-Debians.html
# Add the ROS 2 apt repository
RUN apt update && apt install -y curl gnupg2 lsb-release
RUN curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key  -o /usr/share/keyrings/ros-archive-keyring.gpg
RUN bash -c 'echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(source /etc/os-release && echo $UBUNTU_CODENAME) main" | tee /etc/apt/sources.list.d/ros2.list > /dev/null'

# https://answers.ros.org/question/325039/apt-update-fails-cannot-install-pkgs-key-not-working/
RUN apt-key del 421C365BD9FF1F717815A3895523BAEEB01FA116
# add the new key
RUN apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654
RUN apt clean && apt update

# Downloading ROS 2
RUN apt update && \
    apt install -y ros-${ROS_DISTRO}-desktop \
    ros-${ROS_DISTRO}-ros-base
RUN bash -c 'source /opt/ros/${ROS_DISTRO}/setup.bash'

# install git and other needed libs including catkin build
RUN apt update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends git apt-utils \
    python3-osrf-pycommon \
    curl wget vim less lsof net-tools git htop xterm terminator

RUN bash -c 'apt install curl gnupg2 lsb-release && \
echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list && \
curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | apt-key add -'



# Install gpd
USER ${USER}
RUN cd /opt && rm -rf gpd \
    && sudo git clone https://github.com/icclab/gpd gpd \
    && cd gpd \
    && sudo mkdir build \
    && cd build \
    && sudo cmake ..  \
    && sudo make -j8 \
    && sudo make install

################################################################################

# install updates
USER root
RUN apt update && \
    apt dist-upgrade -y && \
    apt upgrade -y

################################################################################

# update dependencies
RUN apt install -y \
    cmake \
    libbullet-dev \
    clang-format-10 \
    python3-colcon-common-extensions \
    python3-flake8 \
    python3-pip \
    python3-pytest-cov \
    python3-setuptools \
    python3-vcstool \
    python3-rosdep && \
    rosdep init

# https://moveit.ros.org/install-moveit2/binary/
# Install MoveIt and Control
RUN apt install -y ros-foxy-moveit \
    ros-foxy-ros2-control

USER ${USER}
# Create and Switch to the workspace
WORKDIR /home/${USER}
RUN mkdir -p ~/ws/src && cd ~/ws/src && \
    rosdep update

RUN echo "source /opt/ros/${ROS_DISTRO}/setup.bash" >> ~/.bashrc

################################################################################

USER root
COPY entrypoint.sh /etc/entrypoint.sh
RUN chmod 755 /etc/entrypoint.sh
COPY supervisord.conf /etc/supervisord.conf
RUN chmod 755 /etc/supervisord.conf
COPY install_nvidia_drivers.sh /opt/install_nvidia_drivers.sh
RUN chmod 755 /opt/install_nvidia_drivers.sh
RUN /opt/install_nvidia_drivers.sh


EXPOSE 8080
CMD ["/usr/bin/supervisord"]
USER ${USER}


# ament_packace
# colcon build