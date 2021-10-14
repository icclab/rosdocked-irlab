#FROM osrf/ros:noetic-desktop-full
FROM nvidia/opengl:1.2-glvnd-runtime

ARG SOURCEFORGE=https://sourceforge.net/projects
ARG TURBOVNC_VERSION=2.1.2
ARG VIRTUALGL_VERSION=2.5.2
ARG LIBJPEG_VERSION=1.5.2
ARG WEBSOCKIFY_VERSION=0.8.0
ARG NOVNC_VERSION=1.0.0

ENV ROS_DISTRO=noetic
ENV DEBIAN_FRONTEND=noninteractive

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

# Defeat screen locking and power management
# RUN mv /etc/xdg/autostart/light-locker.desktop /etc/xdg/autostart/light-locker.desktop_bak
# RUN mv /etc/xdg/autostart/xfce4-power-manager.desktop /etc/xdg/autostart/xfce4-power-manager.desktop_bak

# Expose whatever port NoVNC will serve from. In our case it will be 40001, see ./start_desktop.sh
EXPOSE 40001
ENV DISPLAY :1

ARG USER=ros

# add ros user to container and make sudoer
RUN useradd -m -s /bin/bash -G video,plugdev ${USER} && \
echo "${USER} ALL=(ALL) NOPASSWD: ALL" > "/etc/sudoers.d/${USER}" && \
chmod 0440 "/etc/sudoers.d/${USER}"


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

USER ros
# Install gpd
RUN cd /opt \
    && sudo git clone https://github.com/icclab/gpd gpd \
    && cd gpd \
    && sudo mkdir build \
    && cd build \
    && sudo cmake ..  \
    && sudo make -j8 \
    && sudo make install
USER "${USER}"


# create catkin ws and clone projects
RUN mkdir -p ~/catkin_ws/src && cd ~/catkin_ws/ && /bin/bash -c "source /opt/ros/${ROS_DISTRO}/setup.bash" && \
cd src && \
git clone https://github.com/icclab/icclab_summit_xl.git -b noetic &&  \
git clone https://github.com/icclab/icclab_grasping_niryo.git -b noetic && \
git clone --branch noetic https://github.com/JenniferBuehler/gazebo-pkgs.git && \
git clone --branch 1.0.0 https://github.com/JenniferBuehler/general-message-pkgs.git && \
#git clone https://github.com/icclab/icclab_turtlebot.git -b ${ROS_DISTRO} && \
#If need two cameras for PCL add -b two_pcl_filtering below
git clone https://github.com/icclab/irlab_point_cloud_filtering.git -b noetic && \
#git clone https://github.com/icclab/laser_filters.git -b indigo-devel && \
git clone --branch gazebo-simulator-noetic https://github.com/icclab/niryo_one_ros.git && \
#git clone --branch 2.2.1 https://github.com/intel-ros/realsense.git && \
#git clone https://github.com/atenpas/gpd.git -b forward && \
git clone https://github.com/icclab/gpd_ros && \
git clone https://github.com/roboticsgroup/roboticsgroup_gazebo_plugins && \
git clone https://github.com/scanse/sweep-sdk.git && \
#git clone https://github.com/utecrobotics/robotiq && \
git clone https://github.com/Danfoa/robotiq_2finger_grippers.git && \
git clone https://github.com/tu-darmstadt-ros-pkg/hector_gazebo.git -b kinetic-devel && \
git clone https://github.com/tu-darmstadt-ros-pkg/hector_models.git -b kinetic-devel && \
git clone -b noetic-devel https://github.com/ros-planning/moveit_visual_tools.git && \
git clone https://github.com/ros-industrial/universal_robot.git && \
git clone https://github.com/ros-perception/depthimage_to_laserscan.git && \
git clone https://github.com/rst-tu-dortmund/costmap_prohibition_layer.git && \
git clone https://github.com/SteveMacenski/spatio_temporal_voxel_layer.git -b noetic-devel && \
git clone https://github.com/iralabdisco/ira_laser_tools.git && \
git clone https://github.com/MoriKen254/timed_roslaunch.git && \
git clone https://github.com/ROBOTIS-GIT/turtlebot3_msgs.git && \
git clone https://github.com/ROBOTIS-GIT/turtlebot3.git && \
git clone https://github.com/ROBOTIS-GIT/turtlebot3_simulations.git && \
git clone https://github.com/SteveMacenski/slam_toolbox.git -b noetic-devel && \
git clone https://github.com/machinekoder/ar_track_alvar.git -b noetic-devel && \
mkdir summit_xl_sources && cd summit_xl_sources && \
git clone https://github.com/RobotnikAutomation/rcomponent.git && \
git clone https://github.com/RobotnikAutomation/robotnik_msgs.git && \
git clone https://github.com/RobotnikAutomation/robotnik_sensors.git -b kinetic-devel && \
git clone https://github.com/RobotnikAutomation/ros-system-monitor && \
git clone https://github.com/RobotnikAutomation/summit_xl_common.git -b melodic-master && \
git clone https://github.com/RobotnikAutomation/summit_xls_ur5_common.git -b kinetic-multirobot-devel && \
git clone https://github.com/RobotnikAutomation/ur_modern_driver.git

#patch for ar_track_alvar on noetic
COPY /issues_solvers/ar_track_alvar* /home/ros/catkin_ws/src/ar_track_alvar/ar_track_alvar/nodes/
# RUN cd ~/catkin_ws/src/ar_track_alvar/ar_track_alvar/nodes && patch < ar_track_alvar_FindBundlesNoKinect.patch && patch < ar_track_alvar_IndNoKinect.patch  && patch < ar_track_alvar_FindBundles.patch && patch < ar_track_alvar_TrainerBundle.patch && patch < ar_track_alvar_IndMarkers.patch

#solve orbecc astra bug in xacro
RUN sed -i 's/<sensor_orbbec_astra_gazebo/<xacro:sensor_orbbec_astra_gazebo/g' /home/ros/catkin_ws/src/summit_xl_sources/robotnik_sensors/urdf/orbbec_astra.urdf.xacro

RUN echo "source ~/catkin_ws/devel/setup.bash" >> ~/.bashrc

#solves the gpd_ros problem not finding opencv2
COPY /issues_solvers/CMakeLists.txt  /home/"${USER}"/catkin_ws/src/gpd_ros

# configure repos for niryo
# RUN cd ~/catkin_ws/src/niryo_one_bringup && git checkout -b gazebo-simulator && git pull origin gazebo-simulator
RUN sudo pip3 install jsonpickle pyquaternion


# add gazebo models to decrease initial gazebo bringup time
RUN mkdir -p ~/.gazebo
ADD .gazebo /home/"${USER}"/.gazebo/
RUN sudo chown ${USER}:${USER} ~/.gazebo/models ; rm -rf /home/ros/catkin_ws/src/robotiq_2finger_grippers/robotiq_modbus_rtu
#RUN cp -r ~/catkin_ws/src/icclab_summit_xl/worlds/models/marker* /home/"${USER}"/.gazebo/models

# update dependencies
RUN sudo apt-get update && DEBIAN_FRONTEND=noninteractive sudo apt-get install -y python3-rosdep \ 
    ros-${ROS_DISTRO}-pcl-ros build-essential g++ python && \
    cd ~/catkin_ws && sudo rosdep init && \
    rosdep update && rosdep install -ry --ignore-packages-from-source --from-paths src 

# install ros-pcl AGAIN. No clue why it doesn't keep it
RUN sudo apt-get install -y python3-pcl ros-${ROS_DISTRO}-pcl-ros ros-${ROS_DISTRO}-moveit-python wget vim 


# build workspace
RUN cd ~/catkin_ws && /bin/bash -c "source /opt/ros/${ROS_DISTRO}/setup.bash && catkin build && source devel/setup.bash"

# Add modified TB3 urdf with 359 scans instead of 360 for the Rplidar to make slam-toolbox work in sim
#RUN cd ~/catkin_ws/src/turtlebot3/turtlebot3_description/urdf  && bash -c "wget https://github.zhaw.ch/raw/RAP-EN/RAP_MAP_LAB_res/master/tb3_urdf/turtlebot3_waffle.gazebo.xacro?token=AAAAQZVGTZ6UTVDZY7IQBADAICXJY -O turtlebot3_waffle.gazebo.xacro && wget https://github.zhaw.ch/raw/RAP-EN/RAP_MAP_LAB_res/master/tb3_urdf/turtlebot3_burger.gazebo.xacro?token=AAAAQZQUP6DRMKY55COBE7TAICXOM -O turtlebot3_burger.gazebo.xacro"
COPY /issues_solvers/turtlebot3_burger.gazebo.xacro /home/"${USER}"/catkin_ws/src/turtlebot3/turtlebot3_description/urdf 
COPY /issues_solvers/turtlebot3_waffle.gazebo.xacro /home/"${USER}"/catkin_ws/src/turtlebot3/turtlebot3_description/urdf


# patch summit_xl old files and add unmerged PRs
RUN bash -c "cd ~/catkin_ws/src/summit_xl_sources/summit_xl_common/summit_xl_description/urdf/wheels ; \
    git checkout remotes/origin/kinetic-devel -- omni_wheel.urdf.xacro" 
#; \
#    bash -c "cd ~/catkin_ws/src/summit_xl_sources/robotnik_sensors; wget -O /tmp/11.patch https://patch-diff.githubusercontent.com/raw/RobotnikAutomation/robotnik_sensors/pull/11.patch; git apply /tmp/11.patch"


COPY /issues_solvers/pick_place_interface.py /opt/ros/noetic/lib/python3/dist-packages/moveit_python

# Switch to the workspace
WORKDIR /home/${USER}


# patch summit_xl old files and add unmerged PRs
RUN bash -c "cd ~/catkin_ws/src/summit_xl_sources/summit_xl_common/summit_xl_description/urdf/wheels ; \
    git checkout remotes/origin/kinetic-devel -- omni_wheel.urdf.xacro"


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



