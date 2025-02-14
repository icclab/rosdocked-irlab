################################################################################
# ZHAW INIT
# Description:  Dockerfile to create the Base CPU Docker image
# Authors:      Leonardo Militano, Mark Straub, Giovanni Toffetti
# Date:         2021-11-08
################################################################################

# Use a more up-to-date base image https://github.com/sloretz/ros_oci_images
FROM ghcr.io/sloretz/ros:jazzy-desktop-full 
# Base image
#FROM osrf/ros:jazzy-desktop-full

################################################################################

# Arguments
ENV ROS_DISTRO=jazzy
ARG USER=ros
ARG uid
ARG home
ARG workspace
ARG shell

################################################################################

# add ros user to container and make sudoer
RUN useradd -m -s /bin/bash -G video,plugdev ${USER} && \
echo "${USER} ALL=(ALL) NOPASSWD: ALL" > "/etc/sudoers.d/${USER}" && \
chmod 0440 "/etc/sudoers.d/${USER}"

# Switch to user
USER "${USER}"

################################################################################

# install git
RUN sudo apt-get update && \
    sudo apt-get install -y wget apt-utils git iproute2

################################################################################

# Only required on BASE CPU
#RUN cd /opt && sudo git clone  https://github.com/icclab/gpd && cd gpd && \
#   sudo mkdir build && cd build && sudo cmake .. && sudo make -j8 && sudo make install

################################################################################

### Install Gazebo Harmonic
RUN sudo curl https://packages.osrfoundation.org/gazebo.gpg --output /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null && \
    sudo apt-get update && sudo apt-get install -y gz-harmonic

# This is required for sharing Xauthority
ENV QT_X11_NO_MITSHM=1
ENV CATKIN_TOPLEVEL_WS="${workspace}/devel"

# Switch to the workspace
WORKDIR ${workspace}
