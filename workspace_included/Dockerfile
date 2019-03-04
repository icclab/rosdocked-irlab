FROM robopaas/rosdocked-kinetic

# Arguments
ENV user=ros
ARG uid
ARG home
ARG workspace
ARG shell

## Clone user into docker image and set up X11 sharing 
#RUN \
#  echo "${user}:x:${uid}:${uid}:${user},,,:${home}:${shell}" >> /etc/passwd && \
#  echo "${user}:x:${uid}:" >> /etc/group && \
#  echo "${user} ALL=(ALL) NOPASSWD: ALL" > "/etc/sudoers.d/${user}" && \
#  chmod 0440 "/etc/sudoers.d/${user}"

# add ros user to container and make sudoer
RUN useradd -m -s /bin/bash -G video,plugdev  ${user} && \
echo "${user} ALL=(ALL) NOPASSWD: ALL" > "/etc/sudoers.d/${user}" && \
chmod 0440 "/etc/sudoers.d/${user}"

# Switch to user
USER "${user}"

# create catkin ws and clone projects
RUN mkdir -p ~/catkin_ws/src && cd ~/catkin_ws/ && /bin/bash -c "source /opt/ros/kinetic/setup.bash && catkin_make" && \
cd src && \
git clone https://github.com/icclab/icclab_summit_xl.git && \
git clone https://github.com/JenniferBuehler/gazebo-pkgs.git && \
git clone https://github.com/JenniferBuehler/general-message-pkgs.git && \
git clone https://github.com/atenpas/gpg.git && \
git clone https://github.com/icclab/icclab_turtlebot.git -b kinetic && \
git clone https://github.com/icclab/irlab_point_cloud_filtering.git -b two_pcl_filtering && \
git clone https://github.com/icclab/laser_filters.git -b indigo-devel && \
git clone https://github.com/NiryoRobotics/niryo_one_ros.git && \
git clone https://github.com/intel-ros/realsense.git -b development && \
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

# patch gpd fwd
RUN cd ~/catkin_ws/src/gpd && \
wget https://patch-diff.githubusercontent.com/raw/atenpas/gpd/pull/63.patch && \
patch < 63.patch

# update dependencies
RUN sudo apt-get update && cd ~/catkin_ws && \
rosdep update && rosdep install -ry --from-paths src 

# realsense / tb3 still missing?
RUN sudo apt-get install -y librealsense2 ros-kinetic-turtlebot3

# build workspace 
RUN cd ~/catkin_ws && /bin/bash -c "source /opt/ros/kinetic/setup.bash && catkin_make"

# edit bashrc
RUN echo "source catkin_ws/devel/setup.bash" >> ~/.bashrc

# This is required for sharing Xauthority
ENV QT_X11_NO_MITSHM=1
ENV CATKIN_TOPLEVEL_WS="${workspace}/devel"
# Switch to the workspace
WORKDIR ${workspace}
