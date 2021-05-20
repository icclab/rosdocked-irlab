#/bin/bash
nvidia-docker run --init --name=ros2-gpu --rm -it -e DISPLAY=:1 -v /tmp/.X11-unix/X0:/tmp/.X11-unix/X0:rw -v $PWD:/home/ros/catkin_ws/src/rap_ros2 --privileged --net host robopaas/rosdocked-foxy-gpu:labs 
