################################################################################
# ZHAW INIT
# Description:  Add required components to the images of CPU and GPU image
# Authors:      Leonardo Militano, Mark Straub, Giovanni Toffetti, Stanislaw Januszko
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
ARG GITHUB_TOKEN

RUN echo "TEST $uid home $home"

# Change folders owner
RUN cd /home/ && \
    chown -R $USER:$USER * && \
    cd ..

# Switch to user
USER "${USER}"

# install git and other needed libs including catkin build
RUN sudo apt update && \
    sudo apt upgrade -y && \
    sudo apt install -y python3-pip ros-${ROS_DISTRO}-tf2-msgs build-essential \
    ros-${ROS_DISTRO}-pcl-ros \
    python3-osrf-pycommon ros-${ROS_DISTRO}-dynamixel-sdk \ 
#    ros-${ROS_DISTRO}-turtlebot3-msgs ros-${ROS_DISTRO}-turtlebot3 \ 
#    ros-${ROS_DISTRO}-turtlebot3-simulations  \
    ros-${ROS_DISTRO}-image-transport-plugins python3-colcon-common-extensions \
    ros-${ROS_DISTRO}-rqt-tf-tree inetutils-ping \
    python3-dev python3-pip python3-venv python3-virtualenv python3-pytest python3-openssl python3-matplotlib python3-tk libpython3-dev \
    python3-flask python3-flask-cors python3-icecream python3-vcstool \
    ros-jazzy-navigation2 ros-jazzy-nav2-bringup ros-jazzy-nav2-controller ros-jazzy-nav2-behavior-tree ros-jazzy-ros-gz-sim ros-jazzy-ros-gz-bridge ros-jazzy-ros-gz-interfaces ros-jazzy-rmw-cyclonedds-cpp ros-jazzy-rtabmap-ros \
    libusb-1.0-0-dev libftdi1-dev libuvc-dev ros-dev-tools

RUN sudo apt install -y --no-install-recommends build-essential ca-certificates cmake \
    software-properties-common lsb-release swig doxygen g++ git libeigen3-dev libgdal-dev libgeos++-dev \
    lcov libgtest-dev libtbb-dev swig libgeos-dev gnuplot libtinyxml2-dev nlohmann-json3-dev gh

# Add environment and colcon utilities to .bashrc
RUN /bin/bash -c 'echo "source /opt/ros/${ROS_DISTRO}/setup.bash" >> ~/.bashrc && \
    echo "source /usr/share/colcon_cd/function/colcon_cd.sh" >> ~/.bashrc && \
    echo "export _colcon_cd_root=/opt/ros/${ROS_DISTRO}/" >> ~/.bashrc && \
    echo "source /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash" >> ~/.bashrc && \
    echo "export GZ_IP=127.0.0.1" >> ~/.bashrc && \
    # echo "export GZ_SIM_RESOURCE_PATH=~/models" >> ~/.bashrc && \
    echo "export GZ_SIM_RESOURCE_PATH=~/colcon_ws/src/mahrbt/mahrbt_py/worlds/models" >> ~/.bashrc && \
    echo "alias srcc=\"source ~/colcon_ws/install/setup.bash\"" >> ~/.bashrc && \
    echo "alias bldc=\"cd ~/colcon_ws/ && colcon build --symlink-install --packages-skip-build-finished\"" >> ~/.bashrc && \
    echo "alias rebldc=\"cd ~/colcon_ws/ && colcon build --symlink-install\"" >> ~/.bashrc && \
    echo "alias cdc=\"cd ~/colcon_ws/\"" >> ~/.bashrc && \
    echo "bldcs() { cd ~/colcon_ws/ && colcon build --symlink-install --packages-select \$1 \$2 \$3 \$4 \$5 \$6 \$7 \$8 \$9; }" >> ~/.bashrc && \
    echo "alias tf=\"clear && srcc && ros2 run tf2_tools view_frames\"" >> ~/.bashrc && \
    echo "alias mapi=\"cd ~/colcon_ws && ros2 run mahroboter_gui mapi\"" >> ~/.bashrc && \
    echo "alias mgui=\"cd ~/non_ros_ws/mahroboter_gui && npm run dev -- --host\"" >> ~/.bashrc && \
    echo "source ~/colcon_ws/install/setup.bash" >> ~/.bashrc'

# Clone Fields2Cover
RUN mkdir -p ~/libraries && \
    cd ~/libraries && \
    git clone https://github.com/Fields2Cover/Fields2Cover.git

# Compile and install Fields2Cover
RUN mkdir -p ~/libraries/Fields2Cover/build && \
    cd ~/libraries/Fields2Cover/build  && \
    cmake -DCMAKE_BUILD_TYPE=Release -DUSE_ORTOOLS_RELEASE=ON -DBUILD_PYTHON=ON ..  && \
    make -j6  && \
    sudo make install

# Run F2C's Python3 bindings tests
RUN cd ~/libraries/Fields2Cover && \
    pytest-3 tests/python/

# Install NodeJS
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash && \
    export NVM_DIR="$HOME/.nvm" && \
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" && \
    [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion" && \
    nvm install 22 && \
    nvm use 22 && \
    nvm alias default 22

# configure repos for niryo
# RUN sudo pip3 install jsonpickle

#RUN mkdir -p ~/colcon_ws/src && cd ~/turtlebot3_ws/ && /bin/bash -c "source /opt/ros/${ROS_DISTRO}/setup.bash" && \
#cd src && \
#git clone -b humble-devel https://github.com/ROBOTIS-GIT/turtlebot3_simulations.git

#RUN cd ~/turtlebot3_ws/ && /bin/bash -c "source /opt/ros/${ROS_DISTRO}/setup.bash" 
#RUN /bin/bash -c "source /opt/ros/humble/setup.bash; mkdir -p ~/colcon_ws/src; cd colcon_ws; colcon build --symlink-install"

# Create colcon_ws and clone Mahroboter-related repositories
RUN mkdir -p ~/colcon_ws/src && cd ~/colcon_ws && /bin/bash -c "source /opt/ros/${ROS_DISTRO}/setup.bash && \
    cd src && \
    git clone https://github.com/IntelligentRoboticsLabs/kobuki.git -b jazzy && \
    vcs import < kobuki/thirdparty.repos && \
    git clone https://oauth2:${GITHUB_TOKEN}@github.zhaw.ch/CloudRobotics/kobuki_ros.git && \
    git clone https://oauth2:${GITHUB_TOKEN}@github.zhaw.ch/CloudRobotics/mahroboter_api.git && \
    git clone https://oauth2:${GITHUB_TOKEN}@github.zhaw.ch/CloudRobotics/mahrbt.git"

RUN rm -rf ~/colcon_ws/src/ThirdParty/kobuki_ros/
RUN rm -rf ~/colcon_ws/src/mahrbt/mahrbt

# update dependencies
RUN sudo apt update && cd ~/colcon_ws && \
    bash -c "if [ ! -f /etc/ros/rosdep/sources.list.d/20-default.list ]; then sudo rosdep init; fi" && \
    rosdep update && rosdep install -ry --ignore-packages-from-source --from-paths src

# install ros-pcl AGAIN. No clue why it doesn't see it
# RUN sudo apt-get update && \
#     sudo apt-get install -y  ros-${ROS_DISTRO}-pcl-ros wget vim 
#ros-${ROS_DISTRO}-moveit-python  doesn't work

# build workspace
# RUN touch COLCON_IGNORE ; cp COLCON_IGNORE ~/colcon_ws/src/ros2_robotiq_gripper/robotiq_driver ; cp COLCON_IGNORE ~/colcon_ws/src/ros2_robotiq_gripper/robotiq_controllers ; cp COLCON_IGNORE ~/colcon_ws/src/ros2_robotiq_gripper/robotiq_hardware_tests
RUN /bin/bash -c "source /opt/ros/${ROS_DISTRO}/setup.bash && cd colcon_ws && colcon build --symlink-install"

COPY env.sh /home/"${USER}"/env.sh
COPY cyclonedds.xml  /home/"${USER}"/cyclonedds.xml
RUN echo "if [ -f "~/env.sh" ]; then source ~/env.sh; fi" >> ~/.bashrc

RUN sudo apt install -y --no-install-recommends terminator
# COPY gazebo /home/"${USER}"/gazebo
# RUN sudo chown -R ros:ros gazebo

# Create non_ros_ws and clone Mahroboter GUI repo (React, ROS-agnostic)
RUN mkdir -p ~/non_ros_ws && cd ~/non_ros_ws && \
    git clone https://oauth2:${GITHUB_TOKEN}@github.zhaw.ch/CloudRobotics/mahroboter_gui.git

#RUN /bin/bash -c "source /opt/ros/${ROS_DISTRO}/setup.bash"
# patch summit_xl old files and add unmerged PRs
#RUN bash -c "cd ~/catkin_ws/src/summit_xl_sources/summit_xl_common/summit_xl_description/urdf/wheels ; \
#    git checkout remotes/origin/kinetic-devel -- omni_wheel.urdf.xacro"
################################################################################
