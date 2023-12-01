#!/bin/bash
# setup ros2 environment
export ROS_DISTRO=humble
source "/opt/ros/$ROS_DISTRO/setup.bash" --
source "/home/ros/colcon_ws/install/setup.bash"
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
export CYCLONEDDS_URI=file:///home/ros/cyclonedds.xml 
echo "** ROS2 $ROS_DISTRO initialized with $RMW_IMPLEMENTATION**"


# launch the robot
launchfile="icclab_tb2_bringup_complete.launch.py"
ros2 launch turtlebot2_bringup $launchfile &
ROS_PID=$!
wait $ROS_PID

