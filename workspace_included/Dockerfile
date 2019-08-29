FROM robopaas/rosdocked-kinetic

# Arguments
ENV user=ros
ARG uid
ARG home
ARG workspace
ARG shell

# update ros.org keys
RUN apt-key del 421C365BD9FF1F717815A3895523BAEEB01FA116 && \
apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654

# add ros user to container and make sudoer
RUN useradd -m -s /bin/bash -G video,plugdev  ${user} && \
echo "${user} ALL=(ALL) NOPASSWD: ALL" > "/etc/sudoers.d/${user}" && \
chmod 0440 "/etc/sudoers.d/${user}"

# Switch to user
USER "${user}"

# create catkin ws and clone projects
RUN mkdir -p ~/catkin_ws/src && cd ~/catkin_ws/ && /bin/bash -c "source /opt/ros/kinetic/setup.bash && catkin build" && \
cd src && \
git clone https://github.com/icclab/icclab_summit_xl.git && \
git clone --branch 1.0.2 https://github.com/JenniferBuehler/gazebo-pkgs.git && \
git clone --branch 1.0.0 https://github.com/JenniferBuehler/general-message-pkgs.git && \
git clone https://github.com/atenpas/gpg.git && \
git clone https://github.com/icclab/icclab_turtlebot.git -b kinetic && \
git clone https://github.com/icclab/irlab_point_cloud_filtering.git -b two_pcl_filtering && \
git clone https://github.com/icclab/laser_filters.git -b indigo-devel && \
git clone https://github.com/NiryoRobotics/niryo_one_ros.git && \
git clone --branch 2.2.1 https://github.com/intel-ros/realsense.git -b development && \
git clone https://github.com/atenpas/gpd.git -b forward && \
mkdir summit_xl_sources && cd summit_xl_sources && \
git clone https://github.com/RobotnikAutomation/rcomponent.git && \
git clone https://github.com/RobotnikAutomation/robotnik_msgs.git && \
git clone https://github.com/RobotnikAutomation/robotnik_sensors.git -b kinetic-multi-devel && \
git clone https://github.com/RobotnikAutomation/ros-system-monitor && \
git clone https://github.com/RobotnikAutomation/summit_xl_common.git -b kinetic-multirobot-devel && \
git clone https://github.com/RobotnikAutomation/summit_xls_ur5_common.git -b indigo-devel && \
git clone https://github.com/scanse/sweep-sdk.git && \
git clone https://github.com/RobotnikAutomation/ur_modern_driver.git

# add gazebo models to decrease initial gazebo bringup time
RUN mkdir -p ~/.gazebo
ADD .gazebo /home/"${user}"/.gazebo/

# patch gpd fwd
RUN cd ~/catkin_ws/src/gpd && \
wget https://patch-diff.githubusercontent.com/raw/atenpas/gpd/pull/63.patch && \
patch < 63.patch

RUN sudo apt-get install -y apt-utils

# update dependencies
RUN sudo apt-get update && cd ~/catkin_ws && \
rosdep update && rosdep install -ry --from-paths src

# Environment variables for noVNC
# Setup demo environment variables
ENV DEBIAN_FRONTEND=noninteractive \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8 \
    LC_ALL=C.UTF-8 \
    DISPLAY=:0.0 \
    DISPLAY_WIDTH=1024 \
    DISPLAY_HEIGHT=768 \
    RUN_FLUXBOX=yes

# Clone noVNC
RUN sudo git clone -b v1.1.0 https://github.com/novnc/noVNC.git /opt/novnc \
    && sudo rm -rf /opt/novnc/.git

# build workspace
RUN cd ~/catkin_ws && /bin/bash -c "source /opt/ros/kinetic/setup.bash && catkin build"

# update gazebo + x11vnc
RUN sudo sh -c 'echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable `lsb_release -cs` main" > /etc/apt/sources.list.d/gazebo-stable.list' && \
wget http://packages.osrfoundation.org/gazebo.key -O - | sudo apt-key add - && \
sudo apt-get update && sudo apt-get install -y gazebo7 x11vnc xvfb fluxbox

# edit bashrc
RUN echo "source catkin_ws/devel/setup.bash" >> ~/.bashrc

# This is required for sharing Xauthority
ENV QT_X11_NO_MITSHM=1
ENV CATKIN_TOPLEVEL_WS="${workspace}/devel"
# Switch to the workspace
WORKDIR ${workspace}

# For noVNC and launching xvfb, x11vnc
EXPOSE 6080

CMD ["sudo", "supervisord", "-c", "/opt/novnc/supervisord/supervisord.conf"]
