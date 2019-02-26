# Rosdocked

## TL;DR

Run our ROS kinetic environment including the workspace and projects

	cd workspace_included
	./run-with-dev.sh

A container (robopaas/rosdocked-kinetic-workspace-included) will be pulled and started, it will have access to your X server.

You can try our projects within it, e.g.:

	roslaunch icclab_summit_xl irlab_sim_summit_xls_complete.launch
	
or

	roslaunch icclab_summit_xl irlab_sim_summit_xls_grasping.launch

The first time you run them Gazebo will have to download all models, so it will take a while and a race condition will prevent arm control. Just restart the script and it will work.


**NOTE** 
If GUI-based apps don't work on your linux you'll have to allow the container to connect to your x-server:

https://www.thegeekstuff.com/2010/06/xhost-cannot-open-display/

(unsafe)  before starting the container, on the host run:

	xhost +

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

### Dockerfile build of deb packages for python point cloud library (PCL)

##### PCL library (point cloud python https://github.com/strawlab/python-pcl) -- avoid re-running, it takes forever!
RUN apt-get update -y && apt-get install -y build-essential devscripts dh-exec python-sphinx doxygen doxygen-latex
RUN add-apt-repository --remove ppa:v-launchpad-jochen-sprickerhof-de/pcl -y && \
dget -u https://launchpad.net/ubuntu/+archive/primary/+files/pcl_1.7.2-14ubuntu1.16.04.1.dsc && \
cd pcl-1.7.2 && DEB_BUILD_OPTIONS=nodocs dpkg-buildpackage -j3 -r -uc -b
RUN dpkg -i *pcl*.deb