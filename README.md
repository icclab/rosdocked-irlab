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

## Without Docker: pixi

The same Summit XL workspace (ROS 2 Jazzy) can run natively on Linux, macOS (Apple
Silicon, macOS 14+) and Windows using [pixi](https://pixi.sh) and the
[RoboStack](https://robostack.github.io) conda packages. No system ROS install or
sudo needed; everything lands in `WORKSPACE/.pixi/`.

Install pixi once (`curl -fsSL https://pixi.sh/install.sh | sh`, or
`winget install prefix-dev.pixi` on Windows), then:

	cd WORKSPACE
	pixi run setup    # once: clone the repos in summit.repos into src/
	pixi shell        # enter the environment (first time downloads a few GB)

Inside `pixi shell` everything works as in the container: `colcon build`,
`ros2 launch icclab_summit_xl summit_xl_simulation_ign.launch.py`, and so on. Open more
terminals with `cd WORKSPACE && pixi shell`. Once built, the workspace's
`install/` is sourced automatically on entering.

There are also shortcuts that run a single command in the environment without
entering it, e.g. `pixi run build`, `pixi run sim`, `pixi run nav`; `pixi task list`
shows them all.

`pixi run setup` also applies `WORKSPACE/patch_src.py`, a couple of local fixes to the
cloned repos (see the file). Linux gets the full stack. On macOS and Windows a few
packages RoboStack does not build are missing (listed at the top of
`WORKSPACE/pixi.toml`); none is needed for the simulation, and on Windows the arm's
MoveIt IK solver is switched from trac_ik to KDL. Only Linux has been tested so far.
