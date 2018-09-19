#FROM ros:kinetic
FROM osrf/ros:kinetic-desktop-full-xenial

# Arguments
ARG user
ARG uid
ARG home
ARG workspace
ARG shell

# Base container has a bunch of old libs, do upgrade
RUN apt-get -y update && apt-get -y upgrade

# Basic Utilities
RUN apt-get -y update && apt-get install -y zsh screen tree sudo ssh

# tentative workaround for realsense camera
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

# Install turtlebot
RUN apt-get -y update && apt-get install -y ros-kinetic-turtlebot-description ros-kinetic-turtlebot ros-kinetic-turtlebot-gazebo ros-kinetic-turtlebot-rviz-launchers

# Latest X11 / mesa GL
RUN apt-get install -y\
  xserver-xorg-dev-lts-wily\
  libegl1-mesa-dev-lts-wily\
  libgl1-mesa-dev-lts-wily\
  libgbm-dev-lts-wily\
  mesa-common-dev-lts-wily\
  libgles2-mesa-lts-wily\
  libwayland-egl1-mesa-lts-wily #libopenvg1-mesa

# Dependencies required to build rviz
RUN apt-get install -y\
  qt4-dev-tools\
  libqt5core5a libqt5dbus5 libqt5gui5 libwayland-client0\
  libwayland-server0 libxcb-icccm4 libxcb-image0 libxcb-keysyms1\
  libxcb-render-util0 libxcb-xkb1 libxkbcommon-x11-0\
  libxkbcommon0

# The rest of ROS-desktop
RUN apt-get install -y ros-kinetic-desktop-full

# Additional development tools + cloud_bridge dependency
RUN apt-get install -y x11-apps python-pip build-essential
RUN pip install catkin_tools defer kombu



# We also need to add a font to rviz for stuff to work: https://answers.ros.org/question/271750/error-when-trying-to-launch-moveit-created-robot-model/
RUN cp  /usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf /opt/ros/kinetic/share/rviz/ogre_media/fonts
COPY liberation.fontdef /opt/ros/kinetic/share/rviz/ogre_media/fonts


## Tof: add stuff for move-it
#RUN apt-get -y update && \
#    apt-get install -y ros-kinetic-moveit ros-kinetic-moveit-visual-tools
#    
## Tof: add stuff for pr2
#RUN apt-get -y update && \
#    apt-get install -y ros-kinetic-pr2-description
#    
## add stuff for Omron robot with arm
#RUN apt-get -y update && \
#    apt-get install -y ros-kinetic-ros-control ros-kinetic-ros-controllers ros-kinetic-gazebo-ros-pkgs ros-kinetic-gazebo-ros-control ros-kinetic-moveit-visual-tools ros-kinetic-moveit ros-kinetic-controller-manager
#    
## Turtlebot arm dependencies + find object
#RUN apt-get -y update && \
#    apt-get install -y ros-kinetic-yocs-math-toolkit ros-kinetic-find-object-2d \
#    ros-kinetic-usb-cam ros-kinetic-rgbd-launch

## GPD plus manipulation components from Lukasz
#RUN apt-get -y update && \
#    apt-get install -y software-properties-common libpcl-dev libprotobuf-dev libleveldb-dev libsnappy-dev libopencv-dev libhdf5-serial-dev protobuf-compiler libgflags-dev libgoogle-glog-dev liblmdb-dev libblas-dev libatlas-dev libatlas-base-dev libpcl-dev libboost-all-dev libeigen3-dev libgflags-dev ros-kinetic-moveit-python # --no-install-recommends
## PCL library (point cloud python https://github.com/strawlab/python-pcl)
#RUN apt-get update -y && apt-get install build-essential devscripts && \
#add-apt-repository -remove ppa:v-launchpad-jochen-sprickerhof-de/pcl -y && \
#dget -u https://launchpad.net/ubuntu/+archive/primary/+files/pcl_1.7.2-14ubuntu1.16.04.1.dsc && \
#cd pcl-1.7.2 && dpkg-buildpackage -r -uc -b && dpkg -i pcl_*.deb
    
# Make SSH available
EXPOSE 22


