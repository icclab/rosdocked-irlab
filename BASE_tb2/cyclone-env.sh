#!/bin/bash
export ROS_DISTRO=humble
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
#export CYCLONEDDS_URI=file:///home/turtlebot/cyclonedds.xml 
#source /opt/ros/$ROS_DISTRO/setup.bash
#sudo chown ros:ros /dev/ttyUSB1
echo "** ROS2 $ROS_DISTRO initialized with $RMW_IMPLEMENTATION**"
