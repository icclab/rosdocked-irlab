################################################################################
# ZHAW INIT
# Description:  Dockerfile to create the Base CPU Docker image
# Authors:      Leonardo Militano, Mark Straub, Giovanni Toffetti
# Date:         2021-11-08
################################################################################

# Base image
FROM ros:jazzy-ros-base

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
# Ubuntu 24.04 images ship a default "ubuntu" user with uid 1000: rename it to ${USER}
# (as in BASE_CPU) so ros keeps uid 1000 like in the humble image. Files written to a
# mounted host folder are owned by uid 1000 on the host, which is the summit user on the robot.
RUN usermod -m -d /home/${USER} -l ${USER} -aG video,plugdev ubuntu && \
groupmod -n ${USER} ubuntu && \
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

# This is required for sharing Xauthority
ENV QT_X11_NO_MITSHM=1
ENV CATKIN_TOPLEVEL_WS="${workspace}/devel"

# Switch to the workspace
WORKDIR ${workspace}

# Switch to user
USER "${USER}"

# install git and other needed libs including catkin build
RUN sudo apt-get update && \
    sudo apt-get install -y python3-pip ros-${ROS_DISTRO}-tf2-msgs build-essential \
    ros-${ROS_DISTRO}-pcl-ros \
    ros-${ROS_DISTRO}-image-transport-plugins python3-colcon-common-extensions \
    inetutils-ping libuvc-dev \
    ros-${ROS_DISTRO}-depthai-ros

# Add environment and colcon utilities to .bashrc
RUN /bin/bash -c 'echo "source /opt/ros/${ROS_DISTRO}/setup.bash" >> ~/.bashrc && \
    echo "source /usr/share/colcon_cd/function/colcon_cd.sh" >> ~/.bashrc && \
    echo "export _colcon_cd_root=/opt/ros/${ROS_DISTRO}/" >> ~/.bashrc && \
    echo "source /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash" >> ~/.bashrc'

# create catkin ws and clone projects
# summit_xl_common has no jazzy branch; humble builds on jazzy (as in WORKSPACE).
# ros_astra_camera: the humble branch does not build on jazzy, rolling does.
RUN mkdir -p ~/colcon_ws/src && cd ~/colcon_ws && /bin/bash -c "source /opt/ros/${ROS_DISTRO}/setup.bash && \
cd src && \
git clone -b jazzy https://github.com/RobotnikAutomation/robotnik_common.git && \
git clone -b humble https://github.com/icclab/summit_xl_common && \
git clone -b ${ROS_DISTRO} https://github.com/icclab/icclab_summit_xl && \
git clone -b ${ROS_DISTRO} https://github.com/icclab/ros2_laser_scan_merger && \
git clone -b jazzy-devel https://github.com/RobotnikAutomation/robotnik_sensors.git && \
git clone -b rolling https://github.com/Juancams/ros_astra_camera && \
git clone https://github.com/PickNikRobotics/ros2_robotiq_gripper.git && \
git clone -b ros2 https://github.com/tylerjw/serial.git"

# update dependencies
RUN sudo apt-get update && cd ~/colcon_ws && \
bash -c "if [ ! -f /etc/ros/rosdep/sources.list.d/20-default.list ]; then sudo rosdep init; fi" && \
rosdep update && rosdep install -ry --ignore-packages-from-source --from-paths src

# install cyclonedds
RUN sudo apt-get update && \
    sudo apt-get install -y ros-${ROS_DISTRO}-pcl-ros wget vim ros-${ROS_DISTRO}-rmw-cyclonedds-cpp nlohmann-json3-dev ros-${ROS_DISTRO}-urg-node

# build workspace
RUN /bin/bash -c "source /opt/ros/${ROS_DISTRO}/setup.bash && cd colcon_ws && colcon build --symlink-install"

# Install Zenoh (install fails because of no systemd in container so we use a workaround)
RUN echo "deb [trusted=yes] https://download.eclipse.org/zenoh/debian-repo/ /" | sudo tee -a /etc/apt/sources.list > /dev/null && \
    sudo apt update && sudo bash -c "apt install -y zenoh-bridge-ros2dds > /dev/null 2>1; echo $?"
