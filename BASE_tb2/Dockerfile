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
    apt-get install -y sudo wget apt-utils git iproute2 python3-colcon-bash python3-rosdep2 python3-colcon-common-extensions

# add ros user to container and make sudoer
RUN useradd -m -s /bin/bash -G video,plugdev ${USER} && \
echo "${USER} ALL=(ALL) NOPASSWD: ALL" > "/etc/sudoers.d/${USER}" && \
chmod 0440 "/etc/sudoers.d/${USER}"

# Switch to the workspace
WORKDIR ${workspace}

# Switch to user
USER "${USER}"
RUN mkdir -p colcon_ws/src && rosdep update

# Add environment and colcon utilities to .bashrc
RUN /bin/bash -c 'echo "source /opt/ros/${ROS_DISTRO}/setup.bash" >> ~/.bashrc && \
    echo "source /usr/share/colcon_cd/function/colcon_cd.sh" >> ~/.bashrc && \
    echo "export _colcon_cd_root=/opt/ros/${ROS_DISTRO}/" >> ~/.bashrc && \
    echo "source /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash" >> ~/.bashrc'

RUN /bin/bash -c "source /opt/ros/${ROS_DISTRO}/setup.bash && \
    cd colcon_ws/src && \
    git clone https://github.com/icclab/TurtleBot2-on-ROS2.git && \
    git clone https://github.com/kobuki-base/kobuki_core.git && \
    git clone https://github.com/icclab/kobuki_ros.git -b humble-test && \
    git clone https://github.com/kobuki-base/kobuki_ros_interfaces.git && \
    git clone https://github.com/CNURobotics/ecl_lite.git -b humble-test && \
    git clone https://github.com/CNURobotics/ecl_core.git -b humble-test && \
    git clone https://github.com/kobuki-base/velocity_smoother.git && \
    git clone https://github.com/kobuki-base/cmd_vel_mux.git && \
    git clone https://github.com/stonier/sophus.git -b release/1.2.x && \
    git clone https://github.com/Juancams/ros_astra_camera -b ros2 && \
    git clone https://github.com/icclab/sllidar_ros2.git && \
    rm -rf TurtleBot2-on-ROS2/turtlebot2_commander && \
    cd .. && \
    rosdep install -ry --from-path src --ignore-src"

RUN sudo apt install -y libudev-dev libjpeg-dev vim && \
    wget https://github.com/libusb/libusb/releases/download/v1.0.26/libusb-1.0.26.tar.bz2 && \
    tar xf libusb-1.0.26.tar.bz2 && \
    /bin/bash -c "cd libusb-1.0.26 && ./configure && make && sudo make install" && \
    rm -rf libusb* && \
    git clone https://github.com/libuvc/libuvc.git && \
    /bin/bash -c "cd libuvc && mkdir build && cd build && \
    cmake -DCMAKE_BUILD_TYPE=Release .. && \
    make && sudo make install" && \
    rm -rf libuvc*

RUN /bin/bash -c "source /opt/ros/${ROS_DISTRO}/setup.bash && \
    cd colcon_ws &&  colcon build --symlink-install"

RUN /bin/bash -c 'echo "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib/" >> ~/.bashrc && \
    echo "source ~/colcon_ws/install/setup.bash" >> ~/.bashrc'

################################################################################


################################################################################

# This is required for sharing Xauthority
ENV QT_X11_NO_MITSHM=1
ENV CATKIN_TOPLEVEL_WS="${workspace}/devel"



