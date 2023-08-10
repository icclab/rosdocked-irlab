export ROS_DISTRO=humble
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
export CYCLONEDDS_URI=file:///${HOME}/cyclonedds.xml 

echo "** ROS2 $ROS_DISTRO initialized with $RMW_IMPLEMENTATION**"
#source install/setup.bash
