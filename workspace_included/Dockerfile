FROM osrf/ros:noetic-desktop-full

# Arguments
ENV user=ros
ENV ROS_DISTRO=noetic

ARG uid
ARG home
ARG workspace
ARG shell

# add ros user to container and make sudoer
RUN useradd -m -s /bin/bash -G video,plugdev  ${user} && \
echo "${user} ALL=(ALL) NOPASSWD: ALL" > "/etc/sudoers.d/${user}" && \
chmod 0440 "/etc/sudoers.d/${user}"

## fix intel librealsense
#RUN apt-get update
## dependencies needed by librealsense. `deb -i` will not resolve these
#RUN apt-get install -y binutils cpp cpp-5 dkms fakeroot gcc gcc-5 kmod libasan2 libatomic1 libc-dev-bin libc6-dev libcc1-0 libcilkrts5 libfakeroot libgcc-5-dev libgmp10 libgomp1 libisl15 libitm1 liblsan0 libmpc3 libmpfr4 libmpx0 libquadmath0 libssl-dev libssl-doc libtsan0 libubsan0 libusb-1.0-0 libusb-1.0-0-dev libusb-1.0-doc linux-headers-4.4.0-159 linux-headers-4.4.0-159-generic linux-headers-generic linux-libc-dev make manpages manpages-dev menu patch zlib1g-dev
#RUN apt-get install -y libssl-dev libssl-doc libusb-1.0-0 libusb-1.0-0-dev libusb-1.0-doc linux-headers-4.4.0-159 linux-headers-4.4.0-159-generic linux-headers-generic zlib1g-dev apt-utils

## modify librealsense deb (unpack, replace script, repack)
#RUN apt-get download ros-${ROS_DISTRO}-librealsense
#RUN dpkg-deb -R ros-${ROS_DISTRO}-librealsense*.deb ros-rslib/
#RUN wget https://gist.githubusercontent.com/dizz/404ef259a15e1410d692792da0c27a47/raw/3769e80a051b5f2ce2a08d4ee6f79c766724f495/postinst
#RUN chmod +x postinst
#RUN cp postinst ros-rslib/DEBIAN
#RUN dpkg-deb -b ./ros-rslib/ ros-${ROS_DISTRO}-librealsense_1.12.1-0xenial-20190830_icrlab_amd64.deb
## install container friendly libsense
#RUN dpkg -i ros-${ROS_DISTRO}-librealsense_1.12.1-0xenial-20190830_icrlab_amd64.deb
## lock from updates
#RUN apt-mark hold ros-${ROS_DISTRO}-librealsense

# Switch to user
USER "${user}"

# install git and other needed libs including catkin build
RUN sudo apt-get update && \
    sudo apt-get install -y git apt-utils \
    ros-${ROS_DISTRO}-pcl-ros python3-catkin-tools \
    python3-osrf-pycommon && \
    sudo apt-get upgrade -y

# create catkin ws and clone projects
RUN mkdir -p ~/catkin_ws/src && cd ~/catkin_ws/ && /bin/bash -c "source /opt/ros/${ROS_DISTRO}/setup.bash" && \
cd src && \
git clone https://github.com/icclab/icclab_summit_xl.git -b noetic-raplabs &&  \
#git clone https://github.com/icclab/icclab_grasping_niryo.git && \
git clone --branch noetic https://github.com/JenniferBuehler/gazebo-pkgs.git && \
git clone --branch 1.0.0 https://github.com/JenniferBuehler/general-message-pkgs.git && \
#git clone https://github.com/icclab/icclab_turtlebot.git -b ${ROS_DISTRO} && \
#If need two cameras for PCL add -b two_pcl_filtering below
#git clone https://github.com/icclab/irlab_point_cloud_filtering.git && \
#git clone https://github.com/icclab/laser_filters.git -b indigo-devel && \
#git clone --branch gazebo-simulator https://github.com/icclab/niryo_one_ros.git && \
#git clone --branch 2.2.1 https://github.com/intel-ros/realsense.git && \
#git clone https://github.com/atenpas/gpd.git -b forward && \
git clone https://github.com/roboticsgroup/roboticsgroup_gazebo_plugins && \
git clone https://github.com/scanse/sweep-sdk.git && \
#git clone https://github.com/utecrobotics/robotiq && \
git clone https://github.com/Danfoa/robotiq_2finger_grippers.git && \
git clone https://github.com/tu-darmstadt-ros-pkg/hector_gazebo.git -b kinetic-devel && \
git clone https://github.com/tu-darmstadt-ros-pkg/hector_models.git -b kinetic-devel && \
git clone -b noetic-devel https://github.com/ros-planning/moveit_visual_tools.git && \
git clone https://github.com/ros-industrial/universal_robot.git && \
git clone https://github.com/ros-perception/depthimage_to_laserscan.git && \
git clone https://github.com/rst-tu-dortmund/costmap_prohibition_layer.git && \
git clone https://github.com/SteveMacenski/spatio_temporal_voxel_layer.git -b noetic-devel && \
git clone https://github.com/iralabdisco/ira_laser_tools.git && \
git clone https://github.com/MoriKen254/timed_roslaunch.git && \
mkdir summit_xl_sources && cd summit_xl_sources && \
git clone https://github.com/RobotnikAutomation/rcomponent.git && \
git clone https://github.com/RobotnikAutomation/robotnik_msgs.git && \
git clone https://github.com/RobotnikAutomation/robotnik_sensors.git -b kinetic-devel && \
git clone https://github.com/RobotnikAutomation/ros-system-monitor && \
git clone https://github.com/RobotnikAutomation/summit_xl_common.git -b kinetic-multirobot-devel && \
git clone https://github.com/RobotnikAutomation/summit_xls_ur5_common.git -b kinetic-multirobot-devel && \
git clone https://github.com/RobotnikAutomation/ur_modern_driver.git && \
git clone https://github.com/SteveMacenski/slam_toolbox.git -b noetic-devel && \
git clone https://github.com/ROBOTIS-GIT/turtlebot3_msgs.git && \
git clone https://github.com/ROBOTIS-GIT/turtlebot3.git && \
git clone https://github.com/ROBOTIS-GIT/turtlebot3_simulations.git 
# configure repos for niryo
# RUN cd ~/catkin_ws/src/niryo_one_bringup && git checkout -b gazebo-simulator && git pull origin gazebo-simulator
# RUN cd ~/catkin_ws/src/irlab_point_cloud_filtering && git checkout -b dev && git pull origin dev

# add gazebo models to decrease initial gazebo bringup time
RUN mkdir -p ~/.gazebo
ADD .gazebo /home/"${user}"/.gazebo/
RUN sudo chown ros:ros ~/.gazebo/models ; rm -rf /home/ros/catkin_ws/src/robotiq_2finger_grippers/robotiq_modbus_rtu
RUN cp -r ~/catkin_ws/src/icclab_summit_xl/worlds/models/marker* /home/"${user}"/.gazebo/models

# update dependencies
RUN sudo apt-get update && cd ~/catkin_ws && \
rosdep update && rosdep install -ry --ignore-packages-from-source --from-paths src 

# install ros-pcl AGAIN. No clue why it doesn't see it
RUN sudo apt-get update && \
    sudo apt-get install -y ros-${ROS_DISTRO}-pcl-ros wget

# build workspace
RUN cd ~/catkin_ws && /bin/bash -c "source /opt/ros/${ROS_DISTRO}/setup.bash && catkin build && source devel/setup.bash"

# patch summit_xl old files and add unmerged PRs
#RUN bash -c "cd ~/catkin_ws/src/summit_xl_sources/summit_xl_common/summit_xl_description/urdf/wheels ; \
#    git checkout remotes/origin/kinetic-devel -- omni_wheel.urdf.xacro" ; \
#    bash -c "cd ~/catkin_ws/src/summit_xl_sources/robotnik_sensors; wget -O /tmp/11.patch https://patch-diff.githubusercontent.com/raw/RobotnikAutomation/robotnik_sensors/pull/11.patch; git apply /tmp/11.patch"

# edit bashrc + workaround for this: https://github.com/SteveMacenski/spatio_temporal_voxel_layer/issues/167
RUN echo "source ~/catkin_ws/devel/setup.bash" >> ~/.bashrc ; \
    echo "export LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libjemalloc.so.2" >> ~/.bashrc \
echo "export TURTLEBOT3_MODEL=burger"

## fix for missing deps - there is prob a better way TODO: reeval this
#RUN sudo apt-get install -y ros-${ROS_DISTRO}-gazebo-ros-pkgs ros-${ROS_DISTRO}-gazebo-ros-control ros-${ROS_DISTRO}-ur-gazebo ros-${ROS_DISTRO}-ur5-moveit-config ros-${ROS_DISTRO}-ur-kinematics ros-${ROS_DISTRO}-timed-roslaunch ros-${ROS_DISTRO}-ira-laser-tools ros-${ROS_DISTRO}-spatio-temporal-voxel-layer

##fix missing dep - jsonpickle
#RUN sudo pip install jsonpickle

# This is required for sharing Xauthority
ENV QT_X11_NO_MITSHM=1
ENV CATKIN_TOPLEVEL_WS="${workspace}/devel"
# Switch to the workspace
WORKDIR ${workspace}

