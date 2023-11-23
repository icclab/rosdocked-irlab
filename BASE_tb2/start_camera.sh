#!/bin/bash
ZENOH_ENDPOINT=$1
ros2 launch turtlebot2_bringup astra_icclab.launch.py & 
ROS_PID=$!
zenoh-bridge-dds -m client -f -e $ZENOH_ENDPOINT &
ZENOH_PID=$!
wait $ROS_PID
wait $ZENOH_PID

