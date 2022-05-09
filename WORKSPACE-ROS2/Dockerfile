################################################################################
# ZHAW INIT
# Description:  Add required components to the images of CPU and GPU image
# Authors:      Leonardo Militano, Mark Straub, Giovanni Toffetti
# Date:         2022-05-06
################################################################################

# Default value
# ARG BASE_IMAGE=robopaas/rosdocked-noetic-baseeee-cpu:latest
ARG BASE_IMAGE
FROM $BASE_IMAGE 

# Arguments
ENV ROS_DISTRO=foxy

USER root

ARG USER=ros
ARG uid
ARG home
ARG workspace
ARG shell

RUN echo "TEST $uid home $home"

# Change folders owner
RUN cd /home/ && \
    chown -R $USER:$USER * && \
    cd ..

# Install projects
RUN apt install -y ros-${ROS_DISTRO}-gazebo-ros-pkgs \
    ros-${ROS_DISTRO}-ros-core \
    ros-${ROS_DISTRO}-geometry2 \
    ros-${ROS_DISTRO}-dynamixel-sdk \
    ros-${ROS_DISTRO}-turtlebot3-msgs \
    ros-${ROS_DISTRO}-turtlebot3


# # add gazebo models to decrease initial gazebo bringup time
# RUN mkdir -p ~/.gazebo
# ADD .gazebo /home/"${USER}"/.gazebo/
# RUN sudo chown $USER:$USER ~/.gazebo/models ; rm -rf /home/$USER/_ws/src/robotiq_2finger_grippers/robotiq_modbus_rtu

# Switch to user
USER "${USER}"
