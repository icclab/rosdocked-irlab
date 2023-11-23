#!/bin/bash
export CYCLONEDDS_URI=file:///home/turtlebot/cyclonedds.xml
launchfile="icclab_tb2_bringup_complete.launch.py"
ros2 launch turtlebot2_bringup $launchfile &
ROS_PID=$!
wait $ROS_PID

