#FROM ros:kinetic
FROM osrf/ros:kinetic-desktop-full-xenial

# Arguments
ARG user
ARG uid
ARG home
ARG workspace
ARG shell

# Basic Utilities
RUN apt-get -y update && apt-get install -y zsh screen tree sudo ssh synaptic

# Latest X11 / mesa GL
RUN apt-get install -y\
  xserver-xorg-dev-lts-wily\
  libegl1-mesa-dev-lts-wily\
  libgl1-mesa-dev-lts-wily\
  libgbm-dev-lts-wily\
  mesa-common-dev-lts-wily\
  libgles2-mesa-lts-wily\
  libwayland-egl1-mesa-lts-wily #libopenvg1-mesa

# Dependencies required to build rviz
RUN apt-get install -y\
  qt4-dev-tools\
  libqt5core5a libqt5dbus5 libqt5gui5 libwayland-client0\
  libwayland-server0 libxcb-icccm4 libxcb-image0 libxcb-keysyms1\
  libxcb-render-util0 libxcb-xkb1 libxkbcommon-x11-0\
  libxkbcommon0

# The rest of ROS-desktop
RUN apt-get install -y ros-kinetic-desktop-full

# Additional development tools
RUN apt-get install -y x11-apps python-pip build-essential
RUN pip install catkin_tools

# Tof: add needed packages for turtlebot
# RUN apt-get -y update && \
#    apt-get install -y ros-kinetic-turtlebot-gazebo \
#    ros-kinetic-turtlebot ros-kinetic-turtlebot-rviz-launchers
RUN pip install defer kombu

# Tof: add stuff for move-it
RUN apt-get -y update && \
    apt-get install -y ros-kinetic-moveit ros-kinetic-moveit-visual-tools
    
# Tof: add stuff for pr2
RUN apt-get -y update && \
    apt-get install -y ros-kinetic-pr2-description
    
# add stuff for Omron robot with arm
RUN apt-get -y update && \
    apt-get install -y ros-kinetic-ros-control ros-kinetic-ros-controllers ros-kinetic-gazebo-ros-pkgs ros-kinetic-gazebo-ros-control ros-kinetic-moveit-visual-tools ros-kinetic-moveit ros-kinetic-controller-manager
    
# Turtlebot arm dependencies + find object
RUN apt-get -y update && \
    apt-get install -y ros-kinetic-yocs-math-toolkit ros-kinetic-find-object-2d \
    ros-kinetic-usb-cam ros-kinetic-rgbd-launch

# workaround for realsense camera
COPY official-source-repositories.list  /etc/apt/sources.list.d/official-source-repositories.list
RUN  apt-get -y update && apt-get install -y ros-kinetic-librealsense

# Install turtlebot
RUN apt-get -y update && apt-get install -y ros-kinetic-turtlebot-description ros-kinetic-turtlebot ros-kinetic-turtlebot-gazebo ros-kinetic-turtlebot-rviz-launchers

# We also need to add a font to rviz for stuff to work: https://answers.ros.org/question/271750/error-when-trying-to-launch-moveit-created-robot-model/
RUN cp  /usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf /opt/ros/kinetic/share/rviz/ogre_media/fonts
COPY liberation.fontdef /opt/ros/kinetic/share/rviz/ogre_media/fonts


# GPD plus manipulation components from Lukasz
RUN apt-get -y update && \
    apt-get install -y software-properties-common libpcl-dev libprotobuf-dev libleveldb-dev libsnappy-dev libopencv-dev libhdf5-serial-dev protobuf-compiler libgflags-dev libgoogle-glog-dev liblmdb-dev libblas-dev libatlas-dev libatlas-base-dev libpcl-dev
RUN apt-get -y update && \
    apt-get install -y  libboost-all-dev libeigen3-dev # --no-install-recommends
    
# Base container has a bunch of old libs, do upgrade
RUN apt-get -y update && apt-get -y upgrade

# Make SSH available
EXPOSE 22


