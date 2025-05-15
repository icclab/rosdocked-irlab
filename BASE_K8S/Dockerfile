# use a more frequently updated base image from here https://github.com/sloretz/ros_oci_images
FROM ghcr.io/sloretz/ros:jazzy-desktop-full
#FROM osrf/ros:jazzy-desktop-noble

# install ros2 packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    ros-jazzy-desktop-full
#\
   # && rm -rf /var/lib/apt/lists/*

# Make sure the package repository is up to date.
#RUN apt-get update && apt-get -y upgrade

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
ENV ROS_DISTRO=jazzy
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

# Update apt sources using mirror
# RUN sed -i -e 's/archive.ubuntu.com/mirror.cloudlab.zhaw.ch/g' /etc/apt/sources.list

# Add custom packages below this comment
#RUN rm /etc/apt/sources.list.d/cuda.list
#RUN apt-key del 7fa2af80
#RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/7fa2af80.pub

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
#        python \
#        python-numpy \
        python3 \
        python3-numpy \
    #    mlocate \
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
#        python \
#        python-numpy \
#        python3 \
#        python3-numpy \
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

## Create user with password ${PASSWD}
#RUN apt-get update && apt-get install --no-install-recommends -y \
#        sudo && \
#    rm -rf /var/lib/apt/lists/* && \
#    #groupadd -g 1000 ${USER} && \
#    #useradd -ms /bin/bash ${USER} -u 1000 -g 1000 && \
#    useradd -ms /bin/bash ${USER} &&\

# Rename ubuntu user and move its home
RUN usermod -m -d /home/${USER} -l ${USER} ubuntu && \
    groupmod -n ${USER} ubuntu && \
    usermod -a -G adm,audio,cdrom,dialout,dip,fax,floppy,input,lp,plugdev,sudo,tape,tty,video,voice ${USER} && \
    echo "${USER} ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers && \
    echo "${USER}:${PASSWD}" | chpasswd && \
    ln -snf "/usr/share/zoneinfo/$TZ" /etc/localtime && echo "$TZ" > /etc/timezone


################################################################################

# set up ROS

# install git and other needed libs including catkin build
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


# update dependencies
RUN sudo apt-get update && DEBIAN_FRONTEND=noninteractive sudo apt-get install -y python3-rosdep \ 
    ros-${ROS_DISTRO}-pcl-ros build-essential g++  ros-${ROS_DISTRO}-pcl-ros  wget vim nvidia-cuda-toolkit

RUN /bin/bash -c "source /opt/ros/${ROS_DISTRO}/setup.bash"

COPY supervisord.conf /etc/supervisord.conf
RUN sudo chmod 755 /etc/supervisord.conf
COPY install_nvidia_drivers.sh /opt/install_nvidia_drivers.sh
RUN sudo chmod 755 /opt/install_nvidia_drivers.sh
RUN sudo /opt/install_nvidia_drivers.sh
COPY entrypoint.sh /etc/entrypoint.sh
RUN sudo chmod 755 /etc/entrypoint.sh

### Install Gazebo Harmonic
RUN sudo curl https://packages.osrfoundation.org/gazebo.gpg --output /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null && \
    sudo apt-get update && sudo apt-get install -y gz-harmonic

### Zenoh

EXPOSE 8080
CMD ["/usr/bin/supervisord"]
COPY MY_RMW_ZENOH_ROUTER_CONFIG.json5 /home/ros/MY_RMW_ZENOH_ROUTER_CONFIG.json5
 
USER ${USER}
WORKDIR /home/${USER}
RUN echo "export RMW_IMPLEMENTATION=rmw_zenoh_cpp" > ~/env_zenoh.sh
RUN echo "export ZENOH_ROUTER_CONFIG_URI=$HOME/MY_RMW_ZENOH_ROUTER_CONFIG.json5" >> ~/env_zenoh.sh
RUN chmod 700 ~/env_zenoh.sh

# Install Zenoh
RUN    sudo apt update && sudo apt install -y ros-${ROS_DISTRO}-rmw-zenoh-cpp



