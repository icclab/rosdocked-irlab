################################################################################
# ZHAW INIT
# Description:  Dockerfile to create the Base CPU Docker image
# Authors:      Leonardo Militano, Mark Straub, Giovanni Toffetti
# Date:         2021-12-09
################################################################################

# Base image
ARG UBUNTU_RELEASE=20.04
FROM nvcr.io/nvidia/cudagl:11.0.3-runtime-ubuntu${UBUNTU_RELEASE}

# https://askubuntu.com/questions/876240/how-to-automate-setting-up-of-keyboard-configuration-package
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
RUN apt-get update && \
    apt-get install -y \ 
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

# Install new cmake (3.22.1 was not working)
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

# Install PCL (Newer versions are not poossible and throw some errors)
RUN cd /opt \
    && wget https://github.com/PointCloudLibrary/pcl/archive/pcl-1.9.0.zip \
    && unzip pcl-1.9.0.zip \
    && cd pcl-pcl-1.9.0 \
    && mkdir build \
    && cd build \
    && cmake -D CMAKE_BUILD_TYPE=None -D BUILD_GPU=ON -D BUILD_apps=ON -D BUILD_examples=ON .. \
    && make -j 8 \
    && make install

# Install Opencv (4.5.4 does not work)
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
USER "${USER}"
RUN cd /opt \
    && sudo git clone https://github.com/icclab/gpd gpd \
    && cd gpd \
    && sudo mkdir build \
    && cd build \
    && sudo cmake ..  \
    && sudo make -j8 \
    && sudo make install


    ################################################################################

# create catkin ws and clone projects
RUN mkdir -p ~/catkin_ws/src && cd ~/catkin_ws/ && /bin/bash -c "source /opt/ros/${ROS_DISTRO}/setup.bash" && \
    cd src && \
    git clone https://github.com/icclab/irlab_point_cloud_filtering.git -b noetic && \
    git clone https://github.com/icclab/gpd_ros

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
