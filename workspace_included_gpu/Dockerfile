# noVNC + TurboVNC + VirtualGL
# Useful links for the software we are using:
# http://novnc.com
# https://turbovnc.org
# https://virtualgl.org

FROM nvidia/opengl:1.2-glvnd-runtime-ubuntu16.04

ARG SOURCEFORGE=https://sourceforge.net/projects
ARG TURBOVNC_VERSION=2.1.2
ARG VIRTUALGL_VERSION=2.5.2
ARG LIBJPEG_VERSION=1.5.2
ARG WEBSOCKIFY_VERSION=0.8.0
ARG NOVNC_VERSION=1.0.0

ENV ROS_DISTRO=kinetic
ENV DEBIAN_FRONTEND=noninteractive
ENV USER=ros

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        ca-certificates \
        curl wget emacs vim less sudo lsof net-tools git htop gedit gedit-plugins \
	unzip zip psmisc xz-utils \
	libglib2.0-0 libxext6 libsm6 libxrender1 \
	libpython-dev libsuitesparse-dev libeigen3-dev libsdl1.2-dev doxygen graphviz libignition-math2-dev \
        gcc \
        libc6-dev \
        libglu1 \
        libglu1:i386 \
        libxv1 \
        libxv1:i386 \
	lubuntu-desktop xvfb xterm terminator zenity mesa-utils \
        make cmake \
        python \
        python-numpy \
        x11-xkb-utils \
        xauth \
        xfonts-base \
        xkb-data && \
    rm -rf /var/lib/apt/lists/*

RUN cd /tmp && \
    curl -fsSL -O ${SOURCEFORGE}/turbovnc/files/${TURBOVNC_VERSION}/turbovnc_${TURBOVNC_VERSION}_amd64.deb \
        -O ${SOURCEFORGE}/libjpeg-turbo/files/${LIBJPEG_VERSION}/libjpeg-turbo-official_${LIBJPEG_VERSION}_amd64.deb \
        -O ${SOURCEFORGE}/virtualgl/files/${VIRTUALGL_VERSION}/virtualgl_${VIRTUALGL_VERSION}_amd64.deb \
        -O ${SOURCEFORGE}/virtualgl/files/${VIRTUALGL_VERSION}/virtualgl32_${VIRTUALGL_VERSION}_amd64.deb && \
    dpkg -i *.deb && \
    rm -f /tmp/*.deb && \
    sed -i 's/$host:/unix:/g' /opt/TurboVNC/bin/vncserver

ENV PATH ${PATH}:/opt/VirtualGL/bin:/opt/TurboVNC/bin

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

# Defeat screen locking and power management
RUN mv /etc/xdg/autostart/light-locker.desktop /etc/xdg/autostart/light-locker.desktop_bak
RUN mv /etc/xdg/autostart/xfce4-power-manager.desktop /etc/xdg/autostart/xfce4-power-manager.desktop_bak

# set up ROS
RUN sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'&& \
    apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654

# install git and other needed libs including catkin build
RUN apt update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends git apt-utils ros-${ROS_DISTRO}-desktop-full \
    curl wget vim less sudo lsof net-tools git htop \
    libxrender1 lubuntu-desktop xvfb xterm terminator zenity mesa-utils \
    x11-xkb-utils xauth make cmake gcc 


# add ros user to container and make sudoer
RUN useradd -m -s /bin/bash -G video,plugdev ${USER} && \
echo "${USER} ALL=(ALL) NOPASSWD: ALL" > "/etc/sudoers.d/${USER}" && \
chmod 0440 "/etc/sudoers.d/${USER}"

# Switch to user
USER "${USER}"

# create catkin ws and clone projects
RUN mkdir -p ~/catkin_ws/src && cd ~/catkin_ws/ && /bin/bash -c "source /opt/ros/kinetic/setup.bash" && \
cd src && \
git clone https://github.com/icclab/icclab_summit_xl.git &&  \
git clone https://github.com/icclab/icclab_grasping_niryo.git && \
git clone --branch 1.0.2 https://github.com/JenniferBuehler/gazebo-pkgs.git && \
git clone --branch 1.0.0 https://github.com/JenniferBuehler/general-message-pkgs.git && \
git clone https://github.com/icclab/icclab_turtlebot.git -b kinetic && \
#If need two cameras for PCL add -b two_pcl_filtering below
git clone https://github.com/icclab/irlab_point_cloud_filtering.git && \
git clone https://github.com/icclab/laser_filters.git -b indigo-devel && \
git clone --branch gazebo-simulator https://github.com/icclab/niryo_one_ros.git && \
git clone --branch 2.2.1 https://github.com/intel-ros/realsense.git && \
git clone https://github.com/atenpas/gpd.git -b forward && \
git clone https://github.com/roboticsgroup/roboticsgroup_gazebo_plugins && \
mkdir summit_xl_sources && cd summit_xl_sources && \
git clone https://github.com/RobotnikAutomation/rcomponent.git && \
git clone https://github.com/RobotnikAutomation/robotnik_msgs.git && \
git clone https://github.com/RobotnikAutomation/robotnik_sensors.git -b kinetic-multi-devel && \
git clone https://github.com/RobotnikAutomation/ros-system-monitor && \
git clone https://github.com/RobotnikAutomation/summit_xl_common.git -b kinetic-multirobot-devel && \
git clone https://github.com/RobotnikAutomation/summit_xls_ur5_common.git -b indigo-devel && \
git clone https://github.com/scanse/sweep-sdk.git && \
git clone https://github.com/RobotnikAutomation/ur_modern_driver.git && \
git clone https://github.com/utecrobotics/robotiq && \
git clone https://github.com/Danfoa/robotiq_2finger_grippers.git 

# configure repos for niryo
# RUN cd ~/catkin_ws/src/niryo_one_bringup && git checkout -b gazebo-simulator && git pull origin gazebo-simulator
# RUN cd ~/catkin_ws/src/irlab_point_cloud_filtering && git checkout -b dev && git pull origin dev

# add gazebo models to decrease initial gazebo bringup time
RUN mkdir -p ~/.gazebo
ADD .gazebo /home/"${USER}"/.gazebo/
RUN sudo chown ${USER}:${USER} ~/.gazebo/models

# patch gpd fwd
RUN cd ~/catkin_ws/src/gpd && \
wget https://patch-diff.githubusercontent.com/raw/atenpas/gpd/pull/63.patch && \
patch < 63.patch


# fix intel librealsense 
# dependencies needed by librealsense. `deb -i` will not resolve these
USER root
RUN apt-get update ; apt-get install -y binutils cpp cpp-5 dkms fakeroot gcc gcc-5 kmod libasan2 libatomic1 libc-dev-bin libc6-dev libcc1-0 libcilkrts5 libfakeroot libgcc-5-dev libgmp10 libgomp1 libisl15 libitm1 liblsan0 libmpc3 libmpfr4 libmpx0 libquadmath0 libssl-dev libssl-doc libtsan0 libubsan0 libusb-1.0-0 libusb-1.0-0-dev libusb-1.0-doc linux-headers-4.4.0-159 linux-headers-4.4.0-159-generic linux-headers-generic linux-libc-dev make manpages manpages-dev menu patch zlib1g-dev libssl-dev libssl-doc libusb-1.0-0 libusb-1.0-0-dev libusb-1.0-doc linux-headers-4.4.0-159 linux-headers-4.4.0-159-generic linux-headers-generic zlib1g-dev apt-utils

# modify librealsense deb (unpack, replace script, repack)
RUN apt-get download ros-kinetic-librealsense
RUN dpkg-deb -R ros-kinetic-librealsense*.deb ros-rslib/
RUN wget https://gist.githubusercontent.com/dizz/404ef259a15e1410d692792da0c27a47/raw/3769e80a051b5f2ce2a08d4ee6f79c766724f495/postinst
RUN chmod +x postinst
RUN cp postinst ros-rslib/DEBIAN
RUN dpkg-deb -b ./ros-rslib/ ros-kinetic-librealsense_1.12.1-0xenial-20190830_icrlab_amd64.deb
# install container friendly libsense
RUN dpkg -i ros-kinetic-librealsense_1.12.1-0xenial-20190830_icrlab_amd64.deb
# lock from updates
RUN apt-mark hold ros-kinetic-librealsense
USER ${USER}

# update dependencies
RUN sudo apt-get update && cd ~/catkin_ws && sudo rosdep init && \
rosdep update && rosdep install -ry --from-paths src

RUN sudo apt update && sudo apt install -y ros-kinetic-catkin python-catkin-tools build-essential g++
# install eigen http://eigen.tuxfamily.org/index.php
RUN cd /tmp && wget  https://gitlab.com/libeigen/eigen/-/archive/3.3.7/eigen-3.3.7.tar.gz && \
tar xzvf eigen-3.3.7.tar.gz && cd eigen-* && mkdir build && cd build && \
cmake .. && sudo make install

USER root
# install opencv 4.1.2
RUN mkdir -p /opt/opencv && cd /opt/opencv && \
    git clone --depth 1 https://github.com/opencv/opencv -b 4.1.2 && \
    git clone --depth 1 https://github.com/opencv/opencv_contrib -b 4.1.2 && \
    cd opencv && mkdir build && cd build && \
    cmake -D CMAKE_BUILD_TYPE=Release -D CMAKE_INSTALL_PREFIX=/usr/local .. && \
    make -j"$(nproc)" && make install
#
## install cmake-3.16.3
RUN cd /opt && wget https://github.com/Kitware/CMake/releases/download/v3.16.3/cmake-3.16.3.tar.gz && \
    tar -xvzf cmake-3.16.3.tar.gz && cd cmake-3.16.3 &&  ./bootstrap -- -DCMAKE_BUILD_TYPE:STRING=Release && make -j8 && make install 

# install caffe ( with GPU: copied from another container https://github.com/intel/caffe/blob/master/docker/standalone/cpu-ubuntu/Dockerfile)
ENV CAFFE_ROOT=/opt/caffe

ENV CUDA_ARCH_BIN "75"
ENV CUDA_ARCH_PTX "75"
RUN apt install -y python-pip software-properties-common libpcl-dev libprotobuf-dev \
  libleveldb-dev libsnappy-dev libhdf5-serial-dev \
  protobuf-compiler libgflags-dev libgoogle-glog-dev liblmdb-dev \
  libblas-dev libatlas-dev libatlas-base-dev libpcl-dev libboost-all-dev \
  libgflags-dev
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
# COPY planning_scene_patch.txt /opt/planning_scene_patch.txt
RUN sudo apt install ros-kinetic-moveit-python
COPY pick_place_interface.py /opt/ros/kinetic/lib/python2.7/dist-packages/moveit_python/

RUN  pip install pyquaternion && \
     patch /usr/lib/python2.7/dist-packages/pyassimp/core.py /opt/pyassimp_patch.txt
#RUN  patch /opt/ros/kinetic/lib/python2.7/dist-packages/moveit_python/planning_scene_interface.py /opt/planning_scene_patch.txt && \ 
RUN pip install cython==0.25.2 && pip install numpy==1.14 && \
 cd /opt && git clone https://github.com/fitter22/python-pcl.git && cd python-pcl && python setup.py build_ext -i && python setup.py install

## add realsense2 camera support
RUN apt-key adv --keyserver keys.gnupg.net --recv-key C8B3A55A6F3EFCDE || apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-key C8B3A55A6F3EFCDE && \
    add-apt-repository "deb http://realsense-hw-public.s3.amazonaws.com/Debian/apt-repo xenial main" -u && \
    apt-get install -y --no-install-recommends librealsense2 librealsense2-dev librealsense2-utils ros-kinetic-ar-track-alvar vim && \
    rm -rf /var/lib/apt/lists/* 

USER ${USER}

# build workspace
RUN cd ~/catkin_ws && /bin/bash -c "source /opt/ros/kinetic/setup.bash && catkin build"

# update gazebo
RUN sudo sh -c 'echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable `lsb_release -cs` main" > /etc/apt/sources.list.d/gazebo-stable.list' && \
wget http://packages.osrfoundation.org/gazebo.key -O - | sudo apt-key add - && \
sudo apt-get update && sudo apt-get install -y gazebo7

# edit bashrc
RUN echo "source ~/catkin_ws/devel/setup.bash" >> ~/.bashrc

# fix for missing deps - there is prob a better way TODO: reeval this
RUN sudo apt-get install -y ros-kinetic-gazebo-ros-pkgs ros-kinetic-gazebo-ros-control ros-kinetic-ur-gazebo ros-kinetic-ur5-moveit-config ros-kinetic-ur-kinematics ros-kinetic-timed-roslaunch ros-kinetic-ira-laser-tools ros-kinetic-spatio-temporal-voxel-layer ros-kinetic-turtlebot-apps ros-kinetic-turtlebot-interactions ros-kinetic-turtlebot-simulator ros-kinetic-ar-track-alvar-msgs

# fix for lower version numpy so pick and place works
RUN sudo rm -rf /usr/lib/python2.7/dist-packages/numpy*
RUN sudo rm -rf /usr/local/lib/python2.7/dist-packages/numpy*
RUN sudo pip install --upgrade numpy==1.16.0

#fix missing dep - jsonpickle
RUN sudo pip install jsonpickle

# Expose whatever port NoVNC will serve from. In our case it will be 40001, see ./start_desktop.sh
EXPOSE 40001
ENV DISPLAY :1

# Switch to the workspace
WORKDIR /home/${USER}

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

