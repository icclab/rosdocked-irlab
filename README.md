# Rosdocked-irlab
A docker container with some of the robotic simulations from the cloud robotics initiative @ ICCLab

## TL;DR

Run our ROS noetic environment including the workspace and projects

	cd WORKSPACE
	docker-compose -f docker-compose-cpu.yml up

A container (robopaas/rosdocked-noetic-cpu:latest) will be pulled and started. 
Another container running noVNC will be started and you'll be able to access it and see the GUI through a browser at: http://localhost

In order to access the container and start our components, in another console, you'll have to find the ros container and enter it, e.g.:
	
	docker ps
	docker exec -it workspace_ros_1 bash

You can try our projects within it, e.g., to run the robot navigation project:

	roslaunch icclab_summit_xl irlab_sim_summit_xls_complete.launch
	
Or to run the grasping project:

	roslaunch icclab_summit_xl irlab_sim_summit_xls_grasping.launch
	
In the browser you will see Gazebo and Rviz and you'll be able to control the robot from there.


## Longer story (Only if you need to rebuild / edit code)

Run ROS Kinetic / Ubuntu Trusty within Docker on Ubuntu Xenial or on any platform with a shared username, home directory, and X11.

This enables you to build and run a persistent ROS Indigo workspace as long as
you can run Docker images.

Note that any changes made outside of your home directory from within the Docker environment will not persist. If you want to add additional binary packages without having to reinstall them each time, add them to the Dockerfile and rebuild.

For more info on Docker see here: https://docs.docker.com/engine/installation/linux/ubuntulinux/

Rather than having devs build the entire image, we split the build logic in two steps:

 - build.sh in the main folder creates a user agnostic container image (robopaas/rosdocked-kinetic:latest)
 -  personalized_image/build.sh adds the current user to the image to mount home dir and access X server


## Build (ICCLab image - optional)

This will create a common image for ICCLab (robopaas/rosdocked-kinetic:latest) still without your user/group ID and home directory.

```
./build.sh
```

## Build personalized image

To add the current user to the image to be able to mount home dir and access X server, run:

	cd personalized_image/
	./build.sh
	
This will pull robopaas/rosdocked-kinetic:latest (hence no need to build it in the optional step)

## Run personalized image

After building, this will run the docker image.

```
./personalized_image/run-with-devs.sh
```

The image shares its  network interface with the host, so you can run this in
multiple terminals for multiple hooks into the docker environment.

Once in the container you should source the devel/setup.bash file in your (kinetic) catkin workspace from your home directory

## Notes on what we added to the Dockerfile

- Turtlebot install files
- Move_it
- Point Cloud library (manually built deb files)
- fake Realsense camera packages (manually built deb files)

## Notes on how we built deb files

### Dockerfile workaround for realsense camera
```
COPY ros-kinetic-librealsense.postinst  /ros-kinetic-librealsense.postinst
COPY ros-kinetic-librealsense.control  /ros-kinetic-librealsense.control
RUN apt-get download ros-kinetic-librealsense && \
mkdir tmp_deb && cd tmp_deb && \
ar p ../ros-kinetic-librealsense_1.12.1-0xenial-20180809-140204-0800_amd64.deb control.tar.gz | tar -xz && \
cp ../ros-kinetic-librealsense.postinst postinst && cp ../ros-kinetic-librealsense.control control && \
cp ../ros-kinetic-librealsense_1.12.1-0xenial-20180809-140204-0800_amd64.deb ../ros-kinetic-librealsense_1.12.1~icclab-0xenial-20180809-140204-0800_amd64.deb && \
tar czf control.tar.gz *[!z] && \
ar r ../ros-kinetic-librealsense_1.12.1~icclab-0xenial-20180809-140204-0800_amd64.deb control.tar.gz && \
cd .. && dpkg -i ros-kinetic-librealsense_1.12.1~icclab-0xenial-20180809-140204-0800_amd64.deb && \
rm -rf /tmp_deb #&&  apt-get remove -y dkms && apt -o APT::Sandbox::User=root update
```

### Dockerfile build of deb packages for python point cloud library (PCL)

##### PCL library (point cloud python https://github.com/strawlab/python-pcl) -- avoid re-running, it takes forever!
```
RUN apt-get update -y && apt-get install -y build-essential devscripts dh-exec python-sphinx doxygen doxygen-latex
RUN add-apt-repository --remove ppa:v-launchpad-jochen-sprickerhof-de/pcl -y && \
dget -u https://launchpad.net/ubuntu/+archive/primary/+files/pcl_1.7.2-14ubuntu1.16.04.1.dsc && \
cd pcl-1.7.2 && DEB_BUILD_OPTIONS=nodocs dpkg-buildpackage -j3 -r -uc -b
RUN dpkg -i *pcl*.deb
```
