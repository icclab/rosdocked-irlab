# Rosdocked-irlab
A docker container with some of the robotic simulations from the cloud robotics initiative @ ICCLab

## TL;DR

Run our ROS humble environment including the workspace and projects on Ubuntu (porting to ROS2 still ongoing)

	cd WORKSPACE
	./run_cpu_xserver.sh

A container (robopaas/rosdocked-humble-cpu:latest) will be pulled and started. 
<!-- Another container running noVNC will be started and you'll be able to access it and see the GUI through a browser at: http://localhost

In order to access the container and start our components, in another console, you'll have to find the ros container and enter it, e.g.:
	
	docker ps
	docker exec -it workspace_ros_1 bash
-->

You can try our projects within it, e.g., to run the robot navigation project:

	ros2 launch icclab_summit_xl summit_xl_simulation.launch.py
	ros2 launch icclab_summit_xl summit_xl_nav2.launch.py rviz:=true
	
<!-- Then you should give an initial position in Rviz for the robot.
Note that the world model is already available and to avoid Gazebo downloading again the models you can export the path as follows:

	export GAZEBO_MODEL_PATH=/opt/ros/humble/share/turtlebot3_gazebo/models -->
