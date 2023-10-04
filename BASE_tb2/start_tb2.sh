#!/bin/bash
ZENOH_ENDPOINT=$1
launchfile="icclab_$(hostname)_bringup_complete.py"
ros2 launch turtlebot2_bringup $launchfile &
ROS_PID=$!
zenoh-bridge-dds -m client -f -e $ZENOH_ENDPOINT &
ZENOH_PID=$!
wait $ROS_PID
wait $ZENOH_PID
