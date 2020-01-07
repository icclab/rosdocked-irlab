#FROM ros:kinetic
FROM osrf/ros:kinetic-desktop-full-xenial

# Arguments
ARG user
ARG uid
ARG home
ARG workspace
ARG shell

# Update basic container, install basic utilities
RUN apt-get -y update && apt-get -y upgrade && apt-get install -y zsh screen tree sudo ssh

# install pre-built deb files (relasense camera + python pcl)
# a previous version of this file shows how to build them
#COPY deb_files /deb_files
#RUN cd /deb_files && wget https://milhouse.cloudlab.zhaw.ch/s/pY8KBeLXkPgqngr && dpkg -i /deb_files/*.deb

## Install turtlebot
#RUN apt-get -y update && apt-get install -y ros-kinetic-turtlebot-description ros-kinetic-turtlebot ros-kinetic-turtlebot-gazebo ros-kinetic-turtlebot-rviz-launchers

# Latest X11 / mesa GL / Dependencies required to build rviz / ROS-desktop
RUN apt-get install -y --no-install-recommends\
    xserver-xorg-dev-lts-wily\
    libegl1-mesa-dev-lts-wily\
    libgl1-mesa-dev-lts-wily\
    libgbm-dev-lts-wily\
    mesa-common-dev-lts-wily\
    libgles2-mesa-lts-wily\
    libwayland-egl1-mesa-lts-wily \
    qt4-dev-tools \
    libqt5core5a libqt5dbus5 libqt5gui5 libwayland-client0\
    libwayland-server0 libxcb-icccm4 libxcb-image0 libxcb-keysyms1\
    libxcb-render-util0 libxcb-xkb1 libxkbcommon-x11-0\
    libxkbcommon0 ros-kinetic-desktop-full x11-apps python-pip build-essential \
    ros-kinetic-moveit ros-kinetic-moveit-visual-tools \
    ros-kinetic-yocs-math-toolkit ros-kinetic-find-object-2d \
    ros-kinetic-usb-cam ros-kinetic-rgbd-launch \
    software-properties-common libpcl-dev libprotobuf-dev \
    libleveldb-dev libsnappy-dev libhdf5-serial-dev \
    protobuf-compiler libgflags-dev libgoogle-glog-dev liblmdb-dev \
    libblas-dev libatlas-dev libatlas-base-dev libpcl-dev libboost-all-dev \
    libgflags-dev ros-kinetic-moveit-python \
    ros-kinetic-ros-control ros-kinetic-ros-controllers ros-kinetic-gazebo-ros-pkgs \
    ros-kinetic-gazebo-ros-control ros-kinetic-moveit-visual-tools \
    ros-kinetic-moveit ros-kinetic-controller-manager \
    python-catkin-tools \
    libignition-math2-dev

RUN pip install catkin_tools \
    defer \
    kombu

# We also need to add a font to rviz for stuff to work: https://answers.ros.org/question/271750/error-when-trying-to-launch-moveit-created-robot-model/
RUN cp  /usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf /opt/ros/kinetic/share/rviz/ogre_media/fonts
COPY liberation.fontdef /opt/ros/kinetic/share/rviz/ogre_media/fonts

# install eigen http://eigen.tuxfamily.org/index.php
RUN cd /tmp && wget  https://gitlab.com/libeigen/eigen/-/archive/3.3.7/eigen-3.3.7.tar.gz && \
tar xzvf eigen-3.3.7.tar.gz && cd eigen-* && mkdir build && cd build && \
cmake .. && make install

# install CUDA 10.2 toolkit required to build caffe GPU
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get install -y keyboard-configuration && \
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/cuda-ubuntu1604.pin && \
    mv cuda-ubuntu1604.pin /etc/apt/preferences.d/cuda-repository-pin-600 && \
    wget http://developer.download.nvidia.com/compute/cuda/10.2/Prod/local_installers/cuda-repo-ubuntu1604-10-2-local-10.2.89-440.33.01_1.0-1_amd64.deb && \
    dpkg -i cuda-repo-ubuntu1604-10-2-local-10.2.89-440.33.01_1.0-1_amd64.deb && \
    rm cuda-repo-ubuntu1604-10-2-local-10.2.89-440.33.01_1.0-1_amd64.deb && \
    apt-key add /var/cuda-repo-10-2-local-10.2.89-440.33.01/7fa2af80.pub && \
    apt-get update && apt-get -y install --no-install-recommends cuda

# install opencv 4.1.2
RUN mkdir -p /opt/opencv && cd /opt/opencv && \
    git clone --depth 1 https://github.com/opencv/opencv -b 4.1.2 && \
    git clone --depth 1 https://github.com/opencv/opencv_contrib -b 4.1.2 && \
    cd opencv && mkdir build && cd build && \
    cmake -D CMAKE_BUILD_TYPE=Release -D CMAKE_INSTALL_PREFIX=/usr/local .. && \
    make -j"$(nproc)" && make install

# install caffe ( with GPU: copied from another container https://github.com/intel/caffe/blob/master/docker/standalone/cpu-ubuntu/Dockerfile)
ENV CAFFE_ROOT=/opt/caffe
ENV CUDA_ARCH_BIN "75"
ENV CUDA_ARCH_PTX "75"
RUN mkdir -p $CAFFE_ROOT && cd $CAFFE_ROOT && \
    git clone --depth 1 https://github.com/fitter22/caffe . && \
    for req in $(cat python/requirements.txt) pydot; do pip install $req; done && \
    mkdir build && cd build && \
    cmake -DCMAKE_BUILD_TYPE=Release -DCUDA_ARCH_NAME=Manual -DCUDA_ARCH_BIN="${CUDA_ARCH_BIN}" -DCUDA_ARCH_PTX="${CUDA_ARCH_PTX}" -DCUDA_NVCC_FLAGS="-O3" \
    -DUSE_CUDNN=ON -DUSE_OPENCV=ON -DBUILD_SHARED_LIBS=ON .. && \
    make all -j"$(nproc)" && make install 
ENV PYCAFFE_ROOT $CAFFE_ROOT/python
ENV PYTHONPATH $PYCAFFE_ROOT:$PYTHONPATH
ENV PATH $CAFFE_ROOT/build/tools:$PYCAFFE_ROOT:$PATH
ENV CAFFE_DIR=$CAFFE_ROOT/build
RUN echo "$CAFFE_ROOT/build/lib" >> /etc/ld.so.conf.d/caffe.conf && ldconfig
# do the actual install in /usr
RUN cp -r $CAFFE_DIR/install/* /usr

# install grasp pose generator (gpg)
RUN mkdir -p /opt/gpg && cd /opt/gpg && \
    git clone https://github.com/atenpas/gpg.git && \
    cd gpg && mkdir build && cd build && cmake .. && \
    make && make install

# install other dependencies for gpd + fix f***ing pyassimp + python-pcl
COPY pyassimp_patch.txt /opt/pyassimp_patch.txt
COPY planning_scene_patch.txt /opt/planning_scene_patch.txt
COPY pick_place_interface.py /opt/ros/kinetic/lib/python2.7/dist-packages/moveit_python
RUN pip install pyquaternion && patch /usr/lib/python2.7/dist-packages/pyassimp/core.py /opt/pyassimp_patch.txt && patch /opt/ros/kinetic/lib/python2.7/dist-packages/moveit_python/planning_scene_interface.py /opt/planning_scene_patch.txt && cd /opt && git clone https://github.com/strawlab/python-pcl.git && cd python-pcl && git checkout 9491615033f85db317c9e29b6a9fe89603f97365 && pip install cython==0.25.2 && pip install numpy==1.14 && python setup.py build_ext -i && python setup.py install

# add realsense2 camera support
RUN apt-key adv --keyserver keys.gnupg.net --recv-key C8B3A55A6F3EFCDE || apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-key C8B3A55A6F3EFCDE && \
    add-apt-repository "deb http://realsense-hw-public.s3.amazonaws.com/Debian/apt-repo xenial main" -u && \
    apt-get install -y --no-install-recommends librealsense2 librealsense2-dev librealsense2-utils ros-kinetic-ar-track-alvar vim && \
    rm -rf /var/lib/apt/lists/*
    

# Make SSH available
EXPOSE 22


