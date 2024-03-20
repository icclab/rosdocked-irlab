#!/bin/bash
launchfile="tb2_complete_no_map.launch.py"
ros2 launch turtlebot2_bringup $launchfile &
ROS_PID=$!
wait $ROS_PID
