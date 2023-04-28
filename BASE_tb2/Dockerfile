################################################################################
# ZHAW INIT
# Description:  Dockerfile to create the Base Docker image on our Turtlebot2
# Authors:      Leonardo Militano, Mark Straub, Giovanni Toffetti
# Date:         2023-04-258
################################################################################

# Base image
FROM ros:humble-ros-base

################################################################################

# Arguments
ENV ROS_DISTRO=humble
ARG USER=ros
ARG uid
ARG home
ARG workspace
ARG shell

################################################################################
# install sudo and git
RUN apt-get update && \
    apt-get install -y sudo wget apt-utils git iproute2 python3-colcon-bash python3-rosdep2

# add ros user to container and make sudoer
RUN useradd -m -s /bin/bash -G video,plugdev ${USER} && \
echo "${USER} ALL=(ALL) NOPASSWD: ALL" > "/etc/sudoers.d/${USER}" && \
chmod 0440 "/etc/sudoers.d/${USER}"

# Switch to the workspace
WORKDIR ${workspace}

# Switch to user
USER "${USER}"
RUN mkdir -p colcon_ws/src && rosdep update
RUN /bin/bash -c "source /opt/ros/${ROS_DISTRO}/setup.bash && \
    cd colcon_ws/src && \
    git clone https://github.com/igrak34/TurtleBot2-on-ROS2.git && \
    git clone https://github.com/kobuki-base/kobuki_core.git && \
    git clone https://github.com/CNURobotics/kobuki_ros.git && \
    git clone https://github.com/kobuki-base/kobuki_ros_interfaces.git && \
    git clone https://github.com/CNURobotics/ecl_lite.git -b humble-test && \
    git clone https://github.com/CNURobotics/ecl_core.git -b humble-test && \
    git clone https://github.com/kobuki-base/velocity_smoother.git && \
    git clone https://github.com/kobuki-base/cmd_vel_mux.git && \
    git clone https://github.com/stonier/sophus.git -b release/1.2.x && \
    rm -rf TurtleBot2-on-ROS2/turtlebot2_commander && \
    cd .. && \
    rosdep install -ry --from-path src --ignore-src"
#RUN /bin/bash -c "source /opt/ros/${ROS_DISTRO}/setup.bash && \
#    cd colcon_ws &&  colcon build"

################################################################################


################################################################################

# This is required for sharing Xauthority
ENV QT_X11_NO_MITSHM=1
ENV CATKIN_TOPLEVEL_WS="${workspace}/devel"



