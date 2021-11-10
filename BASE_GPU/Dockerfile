################################################################################
# ZHAW INIT
# Description:  Dockerfile to create the Base CPU Docker image
# Authors:      Leonardo Militano, Mark Straub, Giovanni Toffetti
# Date:         2021-11-08
################################################################################

# Base image
FROM nvidia/opengl:1.2-glvnd-runtime-ubuntu20.04

################################################################################

# Arguments
ARG SOURCEFORGE=https://sourceforge.net/projects
ARG TURBOVNC_VERSION=2.1.2
ARG VIRTUALGL_VERSION=2.5.2
ARG LIBJPEG_VERSION=1.5.2
ARG WEBSOCKIFY_VERSION=0.8.0
ARG NOVNC_VERSION=1.0.0

ENV ROS_DISTRO=noetic
ENV DEBIAN_FRONTEND=noninteractive
ENV USER=ros

################################################################################

# install min requirements
RUN apt update && apt-get upgrade -y && \
    apt install -y lsb-release gnupg sudo python3-pip 

# set up ROS
RUN sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'&& \
    apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654

# install git and other needed libs including catkin build
RUN apt update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends git apt-utils ros-${ROS_DISTRO}-desktop-full \
    ros-${ROS_DISTRO}-pcl-ros python3-catkin-tools \
    python3-osrf-pycommon \
    curl wget vim less python lsof net-tools git htop \
    libxrender1 lubuntu-desktop xvfb xterm terminator zenity mesa-utils \
    x11-xkb-utils xauth 

################################################################################

# install turbovnc, virtualgl, noVNC
RUN cd /tmp && \
    curl -fsSL -O ${SOURCEFORGE}/turbovnc/files/${TURBOVNC_VERSION}/turbovnc_${TURBOVNC_VERSION}_amd64.deb \
        -O ${SOURCEFORGE}/libjpeg-turbo/files/${LIBJPEG_VERSION}/libjpeg-turbo-official_${LIBJPEG_VERSION}_amd64.deb \
        -O ${SOURCEFORGE}/virtualgl/files/${VIRTUALGL_VERSION}/virtualgl_${VIRTUALGL_VERSION}_amd64.deb \
        -O ${SOURCEFORGE}/virtualgl/files/${VIRTUALGL_VERSION}/virtualgl32_${VIRTUALGL_VERSION}_amd64.deb && \
    dpkg -i *.deb && \
    rm -f /tmp/*.deb && \
    sed -i 's/$host:/unix:/g' /opt/TurboVNC/bin/vncserver

ENV PATH ${PATH}:/opt/VirtualGL/bin:/opt/TurboVNC/bin

RUN apt install -y --no-install-recommends make cmake gcc

RUN curl -fsSL https://github.com/novnc/noVNC/archive/v${NOVNC_VERSION}.tar.gz | tar -xzf - -C /opt && \
    curl -fsSL https://github.com/novnc/websockify/archive/v${WEBSOCKIFY_VERSION}.tar.gz | tar -xzf - -C /opt && \
    mv /opt/noVNC-${NOVNC_VERSION} /opt/noVNC && \
    chmod -R a+w /opt/noVNC && \
    mv /opt/websockify-${WEBSOCKIFY_VERSION} /opt/websockify && \
    cd /opt/websockify && make && \
    cd /opt/noVNC/utils && \
    ln -s /opt/websockify

COPY xorg.conf /etc/X11/xorg.conf
COPY index.html /opt/noVNC/index.html

################################################################################

# add ros user to container and make sudoer
RUN useradd -m -s /bin/bash -G video,plugdev ${USER} && \
echo "${USER} ALL=(ALL) NOPASSWD: ALL" > "/etc/sudoers.d/${USER}" && \
chmod 0440 "/etc/sudoers.d/${USER}"

################################################################################

# Change to root and install requirements
USER root
RUN apt-get install -y \
  software-properties-common \
  ca-certificates \
  wget
RUN wget -O - http://apt.llvm.org/llvm-snapshot.gpg.key | apt-key add -
RUN apt-add-repository "deb http://apt.llvm.org/xenial/ llvm-toolchain-xenial-4.0 main"
RUN add-apt-repository "deb http://security.ubuntu.com/ubuntu xenial-security main"
RUN apt-get update
RUN apt-get install -y \
    build-essential \
    cmake \
    cmake-curses-gui \
    g++ \
    python-dev \
    autotools-dev \
    libicu-dev \
    libbz2-dev \
    libboost-all-dev

RUN apt-get install -y  \
    mc \
    lynx \
    libqhull* \
    pkg-config \
    libxmu-dev \
    libxi-dev \
    --no-install-recommends --fix-missing

RUN apt-get install -y  \
    mesa-common-dev \
    vim  \
    git  \
    unzip  \
    mercurial \
    freeglut3-dev \
    libflann-dev \
    --no-install-recommends --fix-missing

RUN apt-get install -y \
    libboost-all-dev \
    libeigen3-dev \
    python \
    libusb-1.0-0-dev \
    libudev-dev \
    doxygen \
    graphviz \
    libgtest-dev \
    libpcap-dev

RUN apt-get install -y \
    libgtk2.0-dev \
    libavcodec-dev \
    libavformat-dev \
    libjpeg.dev \
    libtiff4.dev \
    libswscale-dev \
    libjasper-dev

# Install new cmake
RUN cd /opt \
    && wget https://github.com/Kitware/CMake/releases/download/v3.17.2/cmake-3.17.2-Linux-x86_64.tar.gz \
    && tar zxvf cmake-3.17.2-Linux-x86_64.tar.gz \
    && mv cmake-3.17.2-Linux-x86_64 /opt/cmake-3.17.2 \
    && ln -sf /opt/cmake-3.17.2/bin/*  /usr/bin/

RUN apt-get autoremove

# Install Eigen
RUN cd /opt \
    && git clone https://github.com/eigenteam/eigen-git-mirror eigen \
    && cd eigen \
    && git checkout tags/3.2.0 \
    && mkdir build \
    && cd build \
    && cmake .. \
    && make -j 8 \
    && make install

# Install VTK
RUN apt-get install -y \
    libvtk7-*

# Install PCL
RUN cd /opt \
    && wget https://github.com/PointCloudLibrary/pcl/archive/pcl-1.9.0.zip \
    && unzip pcl-1.9.0.zip \
    && cd pcl-pcl-1.9.0 \
    && mkdir build \
    && cd build \
    && cmake -D CMAKE_BUILD_TYPE=None -D BUILD_GPU=ON -D BUILD_apps=ON -D BUILD_examples=ON .. \
    && make -j 8 \
    && make install

# Install Opencv
RUN cd /opt \
    && wget https://github.com/opencv/opencv/archive/3.4.3.zip \
    && unzip 3.4.3.zip \
    && cd opencv-3.4.3 \
    && mkdir build \
    && cd build \
    && cmake -D WITH_OPENMP=ON -D ENABLE_PRECOMPILED_HEADERS=OFF ..\
    && make -j 8 \
    && make install

# Install CAFFE dependencies
RUN apt-get install -y \
    libprotobuf-dev \
    libleveldb-dev \
    libsnappy-dev \
    libopencv-dev \
    libhdf5-serial-dev \
    protobuf-compiler \
    libboost-all-dev \
    libatlas-base-dev \
    liblmdb-dev \
    libgoogle-glog-dev

RUN apt-get install -y libturbojpeg \
    libturbojpeg0-dev
    # && ln -s /usr/lib/x86_64-linux-gnu/libturbojpeg.so.0.1.0 /usr/lib/x86_64-linux-gnu/libturbojpeg.so

# Install CAFFE
RUN cd /opt \
    && git clone https://github.com/fbottarel/caffe.git
RUN cd /opt/caffe \
    && mkdir build \
    && cd build \
    && cmake -D BUILD_python=OFF \
        -D BUILD_python_layer=OFF \
        -D BLAS=Atlas \
        -D CUDA_rt_LIBRARY=/usr/local/cuda/lib64/libcudart.so \
        -D CMAKE_INSTALL_PREFIX=/usr/local \
        ../ \
    && make -j 8 \
    && make install

# Install gpd
USER ros
RUN cd /opt \
    && sudo git clone https://github.com/icclab/gpd gpd \
    && cd gpd \
    && sudo mkdir build \
    && cd build \
    && sudo cmake ..  \
    && sudo make -j8 \
    && sudo make install
USER "${USER}"

################################################################################

# create catkin ws and clone projects
RUN mkdir -p ~/catkin_ws/src && cd ~/catkin_ws/ && /bin/bash -c "source /opt/ros/${ROS_DISTRO}/setup.bash" && cd / 

RUN echo "source ~/catkin_ws/devel/setup.bash" >> ~/.bashrc

# update dependencies
RUN sudo apt-get update && DEBIAN_FRONTEND=noninteractive sudo apt-get install -y python3-rosdep \ 
    ros-${ROS_DISTRO}-pcl-ros build-essential g++ python && \
    cd ~/catkin_ws && sudo rosdep init && \
    rosdep update && rosdep install -ry --ignore-packages-from-source --from-paths src 

# install ros-pcl AGAIN. No clue why it doesn't keep it
RUN sudo apt-get install -y python3-pcl ros-${ROS_DISTRO}-pcl-ros ros-${ROS_DISTRO}-moveit-python wget vim 

################################################################################

# build workspace
RUN cd ~/catkin_ws && /bin/bash -c "source /opt/ros/${ROS_DISTRO}/setup.bash && catkin build && source devel/setup.bash"

# Switch to the workspace
WORKDIR /home/${USER}

################################################################################

# Expose whatever port NoVNC will serve from. In our case it will be 40001, see ./start_desktop.sh
EXPOSE 40001
ENV DISPLAY :1


# Defeat screen locking and power management
RUN sudo mv /etc/xdg/autostart/lxqt-xscreensaver-autostart.desktop /etc/xdg/autostart/lxqt-xscreensaver-autostart.desktop_bak && \
    sudo mv /etc/xdg/autostart/lxqt-powermanagement.desktop /etc/xdg/autostart/lxqt-powermanagement.desktop_bak && \
    sudo mv /etc/xdg/autostart/upg-notifier-autostart.desktop /etc/xdg/autostart/upg-notifier-autostart.desktop_bak
    
# Install desktop file for this user
RUN mkdir -p /home/${USER}/Desktop
COPY ./terminator.desktop /home/${USER}/Desktop/
RUN sudo chown ${USER}:${USER} /home/${USER}/Desktop/terminator.desktop
RUN mkdir -p /home/${USER}/.config/terminator
COPY ./terminator_config /home/${USER}/.config/terminator/config
COPY ./self.pem /home/${USER}/self.pem
RUN sudo chown ${USER}:${USER} /home/${USER}/self.pem

# Precede bash on all new terminator shells with vglrun so that 3d graphics apps will use the GPU
RUN sudo perl -pi -e 's/^Exec=terminator$/Exec=terminator -e "vglrun bash"/g' /usr/share/applications/terminator.desktop

# setup the X session started by turbovnc
RUN mkdir -p /home/${USER}/.vnc
COPY ./xstartup.turbovnc /home/${USER}/.vnc/xstartup.turbovnc
RUN sudo chown ${USER}:${USER} /home/${USER}/.vnc/xstartup.turbovnc

COPY start_desktop.sh /usr/local/bin/start_desktop.sh
CMD /usr/local/bin/start_desktop.sh
