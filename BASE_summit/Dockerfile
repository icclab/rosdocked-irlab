################################################################################
# ZHAW INIT
# Description:  Dockerfile to create the Base CPU Docker image
# Authors:      Leonardo Militano, Mark Straub, Giovanni Toffetti
# Date:         2021-11-08
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
    inetutils-ping libuvc-dev libasio-dev  ros-${ROS_DISTRO}-robot-localization \
    ros-${ROS_DISTRO}-nmea-navsat-driver ros-${ROS_DISTRO}-rtabmap-* 

# Add environment and colcon utilities to .bashrc
RUN /bin/bash -c 'echo "source /opt/ros/${ROS_DISTRO}/setup.bash" >> ~/.bashrc && \
    echo "source /usr/share/colcon_cd/function/colcon_cd.sh" >> ~/.bashrc && \
    echo "export _colcon_cd_root=/opt/ros/${ROS_DISTRO}/" >> ~/.bashrc && \
    echo "source /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash" >> ~/.bashrc'


RUN python3 -m pip install depthai

# create catkin ws and clone projects
RUN mkdir -p ~/colcon_ws/src && cd ~/colcon_ws && /bin/bash -c "source /opt/ros/${ROS_DISTRO}/setup.bash && \
cd src && \
git clone -b 4.5.x https://github.com/BehaviorTree/BehaviorTree.CPP.git && \
git clone https://github.com/icclab/ros2_laser_scan_merger.git && \
git clone https://github.com/icclab/liquid_pickup.git && \
git clone https://github.com/icclab/moveit_visual_tools.git -b humble-trajectory-viz && \
git clone -b humble https://github.com/RobotnikAutomation/robotnik_common.git && \
git clone -b humble https://github.com/icclab/summit_xl_common && \
git clone -b humble https://github.com/icclab/icclab_summit_xl && \
git clone -b humble-devel https://github.com/RobotnikAutomation/robotnik_sensors.git && \
git clone https://github.com/Juancams/ros_astra_camera -b humble && \
git clone https://github.com/icclab/add-obstacle-costmap-plugin-layer.git && \
git clone -b humble https://github.com/PickNikRobotics/ros2_robotiq_gripper.git && \
git clone https://github.com/gokulp01/ros2-ublox-zedf9p.git && \
git clone https://github.com/icclab/Zenoh-Perf-Eval.git && \
git clone -b ros2 https://github.com/tylerjw/serial.git && \
git clone https://github.com/icclab/person_detection.git"

# update dependencies
RUN sudo apt-get update && cd ~/colcon_ws && \
bash -c "if [ ! -f /etc/ros/rosdep/sources.list.d/20-default.list ]; then sudo rosdep init; fi" && \
rosdep update && rosdep install -ry --ignore-packages-from-source --from-paths src

# install cyclonedds
RUN  sudo apt-get install -y python3-pcl ros-${ROS_DISTRO}-pcl-ros wget vim ros-${ROS_DISTRO}-rmw-cyclonedds-cpp nlohmann-json3-dev ros-humble-depthai-ros ros-${ROS_DISTRO}-rosbag2-storage-mcap

# Build geographiclib first
RUN /bin/bash -c "source /opt/ros/${ROS_DISTRO}/setup.bash && cd colcon_ws && colcon build --symlink-install --packages-ignore tf_pub"

# build workspace
RUN /bin/bash -c "source /opt/ros/${ROS_DISTRO}/setup.bash && cd colcon_ws && source install/setup.bash && colcon build --symlink-install"

RUN sudo apt-get update && \
    sudo apt-get install -y python3-pip xvfb
    
#RUN sudo apt-get update && \
#    sudo apt-get install -y python3-pip 
RUN sudo pip install vo-wot==0.18.12
# Install Zenoh (install fails because of no systemd in container so we use a workaround)

RUN echo "deb [trusted=yes] https://download.eclipse.org/zenoh/debian-repo/ /" | sudo tee -a /etc/apt/sources.list > /dev/null 
RUN sudo apt update && sudo bash -c "apt install -y zenoh-bridge-ros2dds=1.0.2 > /dev/null 2>1; echo $?"
#RUN sudo apt update && sudo apt install -y ros-humble-rmw-zenoh-cpp
#RUN echo "export RMW_IMPLEMENTATION=rmw_zenoh_cpp"
COPY summit-vo/summit.py /home/ros
COPY summit-vo/summit-td.json /home/ros
COPY summit-vo/summit.yaml /home/ros
COPY summit-vo/minica.pem /home/ros


