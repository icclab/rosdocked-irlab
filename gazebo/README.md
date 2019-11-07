# Procedural Generation for Gazebo

A container with Gazebo (melodic) and https://github.com/boschresearch/pcg_gazebo_pkgs preinstalled.

## Usage

Launch it with the run_with_dev.sh script:

	./run-with-dev.sh
	
Once in the container, source the needed env variables and launch jupyter notebooks as tutorials

	source ~/catkin_ws/devel/setup.bash
	cd src/pcg_gazebo_pkgs/pcg_notebooks/
	jupyter notebook