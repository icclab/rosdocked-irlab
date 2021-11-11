################################################################################
# ZHAW INIT
# Description:  Add required components to the images of CPU and GPU image
# Authors:      Leonardo Militano, Mark Straub, Giovanni Toffetti
# Date:         2021-11-08
################################################################################

# Default value
# ARG BASE_IMAGE=robopaas/rosdocked-noetic-baseeee-cpu:latest
ARG BASE_IMAGE
FROM $BASE_IMAGE 


# Arguments
ENV ROS_DISTRO=noetic

USER root

ENV user=ros
ARG uid
ARG home
ARG workspace
ARG shell

RUN echo "TEST $uid home $home"

# Change folders owner
RUN cd /home/ && \
    chown -R ros:ros * && \
    cd ..

# Switch to user
USER "${user}"

# install git and other needed libs including catkin build
RUN sudo apt-get update && \
    sudo apt-get install -y python3-pip \
    ros-${ROS_DISTRO}-pcl-ros python3-catkin-tools \
    python3-osrf-pycommon

# configure repos for niryo
# RUN sudo pip3 install jsonpickle

# create catkin ws and clone projects
RUN mkdir -p ~/catkin_ws/src && cd ~/catkin_ws/ && /bin/bash -c "source /opt/ros/${ROS_DISTRO}/setup.bash" && \
cd src && \
git clone https://github.com/icclab/icclab_summit_xl.git -b noetic &&  \
git clone https://github.com/icclab/icclab_grasping_niryo.git -b noetic && \
git clone --branch noetic https://github.com/JenniferBuehler/gazebo-pkgs.git && \
git clone --branch 1.0.0 https://github.com/JenniferBuehler/general-message-pkgs.git && \
#git clone https://github.com/icclab/icclab_turtlebot.git -b ${ROS_DISTRO} && \
#If need two cameras for PCL add -b two_pcl_filtering below
git clone https://github.com/icclab/irlab_point_cloud_filtering.git -b noetic && \
#git clone https://github.com/icclab/laser_filters.git -b indigo-devel && \
git clone --branch gazebo-simulator-noetic https://github.com/icclab/niryo_one_ros.git && \
#git clone --branch 2.2.1 https://gitS-GIT/turtlebot3.git && \
git clone https://github.com/ROBOTIS-GIT/turtlebot3_simulations.git && \
git clone https://github.com/SteveMacenski/slam_toolbox.git -b noetic-devel && \
git clone https://github.com/machinekoder/ar_track_alvar.git -b noetic-devel && \
git clone https://github.com/intel-ros/realsense.git && \
git clone https://github.com/icclab/gpd_ros && \
git clone https://github.com/roboticsgroup/roboticsgroup_gazebo_plugins && \
git clone https://github.com/scanse/sweep-sdk.git && \
git clone https://github.com/Danfoa/robotiq_2finger_grippers.git && \
git clone https://github.com/tu-darmstadt-ros-pkg/hector_gazebo.git -b kinetic-devel && \
git clone https://github.com/tu-darmstadt-ros-pkg/hector_models.git -b kinetic-devel && \
git clone -b noetic-devel https://github.com/ros-planning/moveit_visual_tools.git && \
git clone https://github.com/ros-industrial/universal_robot.git && \
git clone https://github.com/ros-perception/depthimage_to_laserscan.git && \
git clone https://github.com/rst-tu-dortmund/costmap_prohibition_layer.git && \
git clone https://github.com/SteveMacenski/spatio_temporal_voxel_layer.git -b noetic-devel && \
git clone https://github.com/iralabdisco/ira_laser_tools.git && \
git clone https://github.com/MoriKen254/timed_roslaunch.git && \
git clone https://github.com/ROBOTIS-GIT/turtlebot3_msgs.git && \
mkdir summit_xl_sources && cd summit_xl_sources && \
git clone https://github.com/RobotnikAutomation/rcomponent.git && \
git clone https://github.com/RobotnikAutomation/robotnik_msgs.git && \
git clone https://github.com/RobotnikAutomation/robotnik_sensors.git -b kinetic-devel && \
git clone https://github.com/RobotnikAutomation/ros-system-monitor && \
git clone https://github.com/RobotnikAutomation/summit_xls_ur5_common.git -b kinetic-multirobot-devel && \
git clone https://github.com/RobotnikAutomation/summit_xl_common.git -b melodic-master && \
git clone https://github.com/RobotnikAutomation/ur_modern_driver.git


COPY /issues_solvers/pick_place_interface.py /opt/ros/noetic/lib/python3/dist-packages/moveit_python
# Add modified TB3 urdf with 359 scans instead of 360 for the Rplidar to make slam-toolbox work in sim
COPY /issues_solvers/turtlebot3_burger.gazebo.xacro  /home/"${user}"/catkin_ws/src/turtlebot3/turtlebot3_description/urdf
COPY /issues_solvers/turtlebot3_waffle.gazebo.xacro   /home/"${user}"/catkin_ws/src/turtlebot3/turtlebot3_description/urdf


# edit bashrc + workaround for this: https://github.com/SteveMacenski/spatio_temporal_voxel_layer/issues/167
RUN echo "source ~/catkin_ws/devel/setup.bash" >> ~/.bashrc ; \
    echo 'export LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libjemalloc.so.2:$LD_PRELOAD' >> ~/.bashrc \
echo "export TURTLEBOT3_MODEL=burger" >> ~/.bashrc


#solve orbecc astra bug in xacro
RUN sed -i 's/<sensor_orbbec_astra_gazebo/<xacro:sensor_orbbec_astra_gazebo/g' /home/ros/catkin_ws/src/summit_xl_sources/robotnik_sensors/urdf/orbbec_astra.urdf.xacro

RUN echo "source ~/catkin_ws/devel/setup.bash" >> ~/.bashrc

# configure repos for niryo
# RUN cd ~/catkin_ws/src/niryo_one_bringup && git checkout -b gazebo-simulator && git pull origin gazebo-simulator

#should solve the gpd_ros problem not finding opencv2
COPY /issues_solvers/CMakeLists.txt  /home/"${user}"/catkin_ws/src/gpd_ros

RUN sudo pip3 install jsonpickle pyquaternion

# add gazebo models to decrease initial gazebo bringup time
RUN mkdir -p ~/.gazebo
ADD .gazebo /home/"${user}"/.gazebo/
RUN sudo chown ros:ros ~/.gazebo/models ; rm -rf /home/ros/catkin_ws/src/robotiq_2finger_grippers/robotiq_modbus_rtu
#RUN cp -r ~/catkin_ws/src/icclab_summit_xl/worlds/models/marker* /home/"${user}"/.gazebo/models

# update dependencies
RUN sudo apt-get update && cd ~/catkin_ws && \
rosdep update && rosdep install -ry --ignore-packages-from-source --from-paths src

# install ros-pcl AGAIN. No clue why it doesn't see it
RUN sudo apt-get update && \
    sudo apt-get install -y python3-pcl ros-${ROS_DISTRO}-pcl-ros ros-${ROS_DISTRO}-moveit-python wget vim


# build workspace
RUN cd ~/catkin_ws && /bin/bash -c "source /opt/ros/${ROS_DISTRO}/setup.bash && catkin build && source devel/setup.bash"

# patch summit_xl old files and add unmerged PRs
RUN bash -c "cd ~/catkin_ws/src/summit_xl_sources/summit_xl_common/summit_xl_description/urdf/wheels ; \
    git checkout remotes/origin/kinetic-devel -- omni_wheel.urdf.xacro"
