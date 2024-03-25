#!/bin/bash
set -e

# setup ros2 environment
source "/opt/ros/$ROS_DISTRO/setup.bash" --
source "/home/ros/colcon_ws/install/setup.bash"
exec "$@"

vo-wot -t tb2-td.json -f tb2.yaml tb2.py &
VOWOT_PID=$!
launchfile="tb2_complete_no_map.launch.py"
ros2 launch turtlebot2_bringup $launchfile &
ROS_PID=$!
/home/ros/zenoh-bridge-ros1dds -c zenoh-bridge-conf.json5 &
ZENOH_PID=$!
wait $ROS_PID
wait $ZENOH_PID
wait $VOWOT_PID


