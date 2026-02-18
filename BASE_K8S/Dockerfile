################################################################################
# ZHAW INIT
# Description:  Dockerfile to create the Base K8S Docker image
# Authors:      Leonardo Militano, Mark Straub, Giovanni Toffetti
# Date:         2021-11-08
################################################################################

# use official ROS Humble image as base (see https://hub.docker.com/r/osrf/ros)
FROM osrf/ros:humble-desktop-full

# install ros2 packages (ensure latest)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ros-humble-desktop-full
#\
   # && rm -rf /var/lib/apt/lists/*

RUN apt-get install -y  \
    make \
    git \
    gcc \
    g++ \
    python3 \
    sudo \
    pciutils \
    cmake \
    ubuntu-drivers-common \
    wget

# Arguments
ENV ROS_DISTRO=humble
ENV DEBIAN_FRONTEND=noninteractive
ENV USER=ros

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

# Update apt sources using mirror
# RUN sed -i -e 's/archive.ubuntu.com/mirror.cloudlab.zhaw.ch/g' /etc/apt/sources.list

# Install locales to prevent errors
RUN apt-get clean && \
    apt-get update && apt-get install --no-install-recommends -y locales && \
    rm -rf /var/lib/apt/lists/* && \
    locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# Install Xorg, XFCE4 Desktop, and others
RUN dpkg --add-architecture i386 && \
    apt-get update && apt-get install --no-install-recommends -y \
        software-properties-common \
        apt-utils \
        build-essential \
        ca-certificates \
        kmod \
        libc6:i386 \
        libc6-dev \
        curl \
        file \
        wget \
        gzip \
        zip \
        unzip \
        gcc \
        git \
        jq \
        make \
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
        xorg-dev \
        iproute2 && \
    apt-get install -y xfce4 xfce4-goodies vulkan-tools && \
    # Remove Bluetooth packages that throw errors
    apt-get autoremove --purge -y \
        blueman \
        pulseaudio-module-bluetooth && \
    rm -rf /var/lib/apt/lists/*

# Install latest noVNC web interface for fallback
RUN apt-get update && apt-get install --no-install-recommends -y \
        autoconf \
        automake \
        autotools-dev \
        chrpath \
        debhelper \
        jq \
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

# Create ros user (osrf/ros base image runs as root with no default ubuntu user)
RUN groupadd -g 1000 ${USER} && \
    useradd -ms /bin/bash ${USER} -u 1000 -g 1000 && \
    usermod -a -G adm,audio,cdrom,dialout,dip,fax,floppy,input,lp,netdev,plugdev,scanner,sudo,tape,tty,video,voice ${USER} && \
    echo "${USER} ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers && \
    echo "${USER}:${PASSWD}" | chpasswd && \
    ln -snf "/usr/share/zoneinfo/$TZ" /etc/localtime && echo "$TZ" > /etc/timezone


################################################################################

# set up ROS

# install git and other needed libs
RUN apt update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends git apt-utils \
    python3-osrf-pycommon \
    curl wget vim less lsof net-tools git htop xterm terminator novnc python3-websockify

# Install gpd
USER $USER
#RUN cd /opt && rm -rf gpd \
 #   && sudo git clone https://github.com/icclab/gpd gpd \
 #   && cd gpd \
 #   && sudo mkdir build \
 #   && cd build \
 #   && sudo cmake ..  \
 #   && sudo make -j8 \
 #   && sudo make install

################################################################################
USER ${USER}
# Switch to the workspace
WORKDIR /home/${USER}

# Install CUDA 12.5 from NVIDIA apt repository
RUN wget -q https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb && \
    sudo dpkg -i cuda-keyring_1.1-1_all.deb && \
    rm cuda-keyring_1.1-1_all.deb && \
    sudo apt-get update && sudo apt-get install -y --no-install-recommends cuda-toolkit-12-5 && \
    sudo rm -rf /var/lib/apt/lists/*

# update dependencies
RUN sudo apt-get update && DEBIAN_FRONTEND=noninteractive sudo apt-get install -y python3-rosdep \
    ros-${ROS_DISTRO}-pcl-ros build-essential g++  ros-${ROS_DISTRO}-pcl-ros  wget vim

RUN /bin/bash -c "source /opt/ros/${ROS_DISTRO}/setup.bash"

# install ros-pcl AGAIN. No clue why it doesn't keep it
RUN sudo apt-get install -y python3-pcl ros-${ROS_DISTRO}-pcl-ros ros-${ROS_DISTRO}-moveit wget vim

COPY supervisord.conf /etc/supervisord.conf
RUN sudo chmod 755 /etc/supervisord.conf
COPY install_nvidia_drivers.sh /opt/install_nvidia_drivers.sh
RUN sudo chmod 755 /opt/install_nvidia_drivers.sh
RUN sudo /opt/install_nvidia_drivers.sh
COPY entrypoint.sh /etc/entrypoint.sh
RUN sudo chmod 755 /etc/entrypoint.sh

EXPOSE 8080
CMD ["/usr/bin/supervisord"]
USER ${USER}
