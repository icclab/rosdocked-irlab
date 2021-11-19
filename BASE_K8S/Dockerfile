################################################################################
# ZHAW INIT
# Description:  Dockerfile to create the Base CPU Docker image
# Authors:      Leonardo Militano, Mark Straub, Giovanni Toffetti
# Date:         2021-11-08
################################################################################

# Base image
FROM ghcr.io/ehfd/nvidia-glx-desktop:latest

################################################################################

# Arguments
ENV ROS_DISTRO=noetic
ENV DEBIAN_FRONTEND=noninteractive
ENV USER=user

################################################################################

# install min requirements
#RUN apt update && apt-get upgrade -y && \
#    apt install -y lsb-release gnupg sudo python3-pip 

USER root
# set up ROS
RUN sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'&& \
    apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654

# install git and other needed libs including catkin build
RUN apt update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends git apt-utils ros-${ROS_DISTRO}-desktop-full \
    ros-${ROS_DISTRO}-pcl-ros python3-catkin-tools \
    python3-osrf-pycommon \
    curl wget vim less lsof net-tools git htop xterm terminator

################################################################################

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
USER $USER
RUN cd /opt && rm -rf gpd \
    && sudo git clone https://github.com/icclab/gpd gpd \
    && cd gpd \
    && sudo mkdir build \
    && cd build \
    && sudo cmake ..  \
    && sudo make -j8 \
    && sudo make install

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


