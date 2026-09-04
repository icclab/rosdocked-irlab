################################################################################
# ZHAW INIT
# Description:  Add required components to the images of CPU and GPU image
# Authors:      Leonardo Militano, Mark Straub, Giovanni Toffetti
# Date:         2021-11-08
################################################################################

# Default value
# ARG BASE_IMAGE=robopaas/rosdocked-noetic-base-cpu:latest
ARG BASE_IMAGE=robopaas/rosdocked-jazzy-base-cpu:latest
FROM $BASE_IMAGE 

# Arguments
ENV ROS_DISTRO=jazzy

USER root

ARG USER
ARG uid
ARG home
ARG workspace
ARG shell

RUN echo "TEST $uid home $home"

# Change folders owner
RUN cd /home/ && \
    chown -R $USER:$USER * && \
    cd ..

# Switch to user
USER "${USER}"

# install git and other needed libs including catkin build
RUN sudo apt-get update && \
    sudo apt-get install -y python3-pip ros-${ROS_DISTRO}-tf2-msgs build-essential \
    ros-${ROS_DISTRO}-pcl-ros \
    python3-osrf-pycommon ros-${ROS_DISTRO}-dynamixel-sdk \ 
#    ros-${ROS_DISTRO}-turtlebot3-msgs ros-${ROS_DISTRO}-turtlebot3 \ 
#    ros-${ROS_DISTRO}-turtlebot3-simulations  \
    ros-${ROS_DISTRO}-image-transport-plugins python3-colcon-common-extensions \
    ros-${ROS_DISTRO}-rqt-tf-tree inetutils-ping

# Add environment and colcon utilities to .bashrc
RUN /bin/bash -c 'echo "source /opt/ros/${ROS_DISTRO}/setup.bash" >> ~/.bashrc && \
    echo "source /usr/share/colcon_cd/function/colcon_cd.sh" >> ~/.bashrc && \
    echo "export _colcon_cd_root=/opt/ros/${ROS_DISTRO}/" >> ~/.bashrc && \
    echo "source /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash" >> ~/.bashrc'

# configure repos for niryo
# RUN sudo pip3 install jsonpickle

#RUN mkdir -p ~/colcon_ws/src && cd ~/turtlebot3_ws/ && /bin/bash -c "source /opt/ros/${ROS_DISTRO}/setup.bash" && \
#cd src && \
#git clone -b humble-devel https://github.com/ROBOTIS-GIT/turtlebot3_simulations.git

#RUN cd ~/turtlebot3_ws/ && /bin/bash -c "source /opt/ros/${ROS_DISTRO}/setup.bash" 
#RUN /bin/bash -c "source /opt/ros/humble/setup.bash; mkdir -p ~/colcon_ws/src; cd colcon_ws; colcon build --symlink-install"

# create catkin ws and clone projects
RUN mkdir -p ~/colcon_ws/src && cd ~/colcon_ws && /bin/bash -c "source /opt/ros/${ROS_DISTRO}/setup.bash && \
cd src && \
# git clone -b humble https://github.com/icclab/summit_xl_sim  && \
# git clone -b humble https://github.com/RobotnikAutomation/robotnik_common.git && \
git clone -b humble https://github.com/icclab/summit_xl_common && \
git clone -b ${ROS_DISTRO} https://github.com/icclab/icclab_summit_xl && \
git clone -b ${ROS_DISTRO} https://github.com/icclab/ros2_laser_scan_merger && \
git clone https://github.com/PickNikRobotics/ros2_robotiq_gripper"

# git clone https://github.com/icclab/TurtleBot2-on-ROS2.git && \
# git clone https://github.com/icclab/kobuki_ros


# update dependencies
RUN sudo apt-get update && cd ~/colcon_ws && \
bash -c "if [ ! -f /etc/ros/rosdep/sources.list.d/20-default.list ]; then sudo rosdep init; fi" && \
rosdep update && rosdep install -ry --ignore-packages-from-source --from-paths src

# install ros-pcl AGAIN. No clue why it doesn't see it
# RUN sudo apt-get update && \
#     sudo apt-get install -y  ros-${ROS_DISTRO}-pcl-ros wget vim 
#ros-${ROS_DISTRO}-moveit-python  doesn't work

# build workspace
RUN touch COLCON_IGNORE ; cp COLCON_IGNORE ~/colcon_ws/src/ros2_robotiq_gripper/robotiq_driver ; cp COLCON_IGNORE ~/colcon_ws/src/ros2_robotiq_gripper/robotiq_controllers ; cp COLCON_IGNORE ~/colcon_ws/src/ros2_robotiq_gripper/robotiq_hardware_tests
# CMAKE_BUILD_TYPE=Release matters: neither colcon nor any of the workspace
# packages set a build type, so without this every C++ node (ros2_laser_scan_merger
# does per-scan pointcloud math) is compiled unoptimised.
# --symlink-install is kept on purpose: students edit packages in place inside
# the container and expect the change to take effect without a full rebuild.
RUN /bin/bash -c "source /opt/ros/${ROS_DISTRO}/setup.bash && cd colcon_ws && \
    colcon build --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=Release"

COPY env.sh /home/"${USER}"/env.sh
COPY cyclonedds.xml  /home/"${USER}"/cyclonedds.xml
RUN echo "if [ -f "~/env.sh" ]; then source ~/env.sh; fi" >> ~/.bashrc

RUN sudo apt install -y --no-install-recommends terminator
# COPY .gazebo /home/ros/.gazebo
# RUN sudo chown -R ros:ros .gazebo

#RUN /bin/bash -c "source /opt/ros/${ROS_DISTRO}/setup.bash"
# patch summit_xl old files and add unmerged PRs
#RUN bash -c "cd ~/catkin_ws/src/summit_xl_sources/summit_xl_common/summit_xl_description/urdf/wheels ; \
#    git checkout remotes/origin/kinetic-devel -- omni_wheel.urdf.xacro"
################################################################################
