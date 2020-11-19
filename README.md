# Ros2docked

## TL;DR

Run a containerized basic ROS2 eloquent  environment and novnc for the graphical interface.
First build the ROS2 foxy container image and then run docker-compose. This will pull the novnc image and run two containers.

	cd rosdocked-irlab
	./build.sh
	docker-compose up

You can access the GUI over a browser using the IP address of your machine and the port number 443 and you will see the RVIZ interface running. You can reduce the RVIZ window to further work with the container.

For more info on Docker see here: https://docs.docker.com/engine/installation/linux/ubuntulinux/

