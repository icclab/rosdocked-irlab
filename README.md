# Rosdocked

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

## Notes on what we added to the Dockerfile

- Turtlebot install files
- Move_it
- Point Cloud library