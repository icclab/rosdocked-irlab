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
RUN apt install -y --no-install-recommends make cmake gcc

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


