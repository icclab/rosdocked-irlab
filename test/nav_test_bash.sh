#!/usr/bin/env bash

# source ROS env
. ~/catkin_ws/devel/setup.bash

# start complete in headless mode 
roslaunch icclab_summit_xl irlab_sim_summit_xls_complete.launch gazebo_gui:=false launch_rviz_nav:=false launch_rviz_grasping:=false & 

# save PID of roslaunch
ROSLAUNCH_PID=$!

# let it start completely
sleep 30
 
# give a navigation goal
rostopic pub -1 /summit_xl/move_base/goal move_base_msgs/MoveBaseActionGoal "header:
  seq: 0
  stamp:
    secs: 0
    nsecs: 0
  frame_id: 'summit_xl_map'
goal_id:
  stamp:
    secs: 0
    nsecs: 0
  id: ''
goal:
  target_pose:
    header:
      seq: 0
      stamp:
        secs: 0
        nsecs: 0
      frame_id: 'summit_xl_map'
    pose:
      position:
        x: 25.0
        y: 4.0
        z: 0.0
      orientation:
        x: 0.0
        y: 0.0
        z: 0.0
        w: 1.0"

# wait for result publication or timeout
RES=`timeout -k 120s 120s rostopic echo -n 1 /summit_xl/move_base/result | grep -c "Goal reached."`

# kill roslaunch
kill -15 $ROSLAUNCH_PID

exit $RES
