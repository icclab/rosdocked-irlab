################################################################################
# ZHAW INIT
# Description:  Add required components to the images of CPU and GPU image
# Authors:      Leonardo Militano, Mark Straub, Giovanni Toffetti
# Date:         2021-11-08
################################################################################

# Default value
# ARG BASE_IMAGE=robopaas/rosdocked-noetic-base-cpu:latest
ARG BASE_IMAGE
FROM $BASE_IMAGE 

# Arguments
ENV ROS_DISTRO=humble

USER root

ARG USER
ARG uid
ARG home
ARG workspace
ARG shell

RUN echo "TEST $uid home $home"

# Change folders owner
RUN cd /home/ && \
    chown -R $USER:$USER * && \
    cd ..

# Switch to user
USER "${USER}"

# install git and other needed libs including catkin build
RUN sudo apt-get update && \
    sudo apt-get install -y python3-pip ros-${ROS_DISTRO}-tf2-msgs build-essential \
    ros-${ROS_DISTRO}-pcl-ros \
    python3-osrf-pycommon ros-${ROS_DISTRO}-dynamixel-sdk \ 
    ros-${ROS_DISTRO}-turtlebot3-msgs ros-${ROS_DISTRO}-turtlebot3 \ 
    ros-${ROS_DISTRO}-turtlebot3-simulations  \
    ros-${ROS_DISTRO}-image-transport-plugins python3-colcon-common-extensions

# Add environment and colcon utilities to .bashrc
RUN /bin/bash -c 'echo "source /opt/ros/${ROS_DISTRO}/setup.bash" >> ~/.bashrc && \
    echo "source /usr/share/colcon_cd/function/colcon_cd.sh" >> ~/.bashrc && \
    echo "export _colcon_cd_root=/opt/ros/${ROS_DISTRO}/" >> ~/.bashrc && \
    echo "source /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash" >> ~/.bashrc'

# configure repos for niryo
# RUN sudo pip3 install jsonpickle

#RUN mkdir -p ~/colcon_ws/src && cd ~/turtlebot3_ws/ && /bin/bash -c "source /opt/ros/${ROS_DISTRO}/setup.bash" && \
#cd src && \
#git clone -b humble-devel https://github.com/ROBOTIS-GIT/turtlebot3_simulations.git

#RUN cd ~/turtlebot3_ws/ && /bin/bash -c "source /opt/ros/${ROS_DISTRO}/setup.bash" 
#RUN /bin/bash -c "source /opt/ros/humble/setup.bash; mkdir -p ~/colcon_ws/src; cd colcon_ws; colcon build --symlink-install"

# create catkin ws and clone projects
RUN mkdir -p ~/colcon_ws/src && cd ~/colcon_ws && /bin/bash -c "source /opt/ros/${ROS_DISTRO}/setup.bash && \
cd src && \
git clone https://github.com/icclab/TurtleBot2-on-ROS2.git && \
git clone -b humble https://github.com/icclab/summit_xl_sim && \
git clone -b humble https://github.com/RobotnikAutomation/robotnik_common.git && \
git clone -b humble https://github.com/icclab/summit_xl_common && \
git clone -b humble-devel https://github.com/RobotnikAutomation/robotnik_sensors.git && \
git clone https://github.com/icclab/kobuki_ros"

#git clone https://github.com/icclab/icclab_grasping_niryo.git -b noetic && \
#git clone --branch noetic https://github.com/JenniferBuehler/gazebo-pkgs.git && \
#git clone --branch 1.0.0 https://github.com/JenniferBuehler/general-message-pkgs.git && \
#git clone https://github.com/icclab/icclab_turtlebot.git -b ${ROS_DISTRO} && \
#If need two cameras for PCL add -b two_pcl_filtering below
#git clone https://github.com/icclab/irlab_point_cloud_filtering.git -b noetic && \
# Required for plugin librealsense_gazebo_plugin.so. Removed because pointclouds are misaligned with plugin
# git clone https://github.com/pal-robotics/realsense_gazebo_plugin && \
#git clone https://github.com/icclab/laser_filters.git -b indigo-devel && \
#git clone --branch gazebo-simulator-noetic https://github.com/icclab/niryo_one_ros.git && \
#git clone https://github.com/SteveMacenski/slam_toolbox.git -b noetic-devel && \
#git clone https://github.com/machinekoder/ar_track_alvar.git -b noetic-devel && \
#git clone -b ros1-legacy https://github.com/intel-ros/realsense.git && \
#git clone https://github.com/icclab/gpd_ros && \
#git clone https://github.com/roboticsgroup/roboticsgroup_gazebo_plugins && \
#git clone https://github.com/Danfoa/robotiq_2finger_grippers.git && \
#git clone https://github.com/tu-darmstadt-ros-pkg/hector_gazebo.git -b kinetic-devel && \
#git clone https://github.com/tu-darmstadt-ros-pkg/hector_models.git -b kinetic-devel && \
#git clone -b noetic-devel https://github.com/ros-planning/moveit_visual_tools.git && \
#git clone https://github.com/ros-perception/depthimage_to_laserscan.git && \
#git clone https://github.com/rst-tu-dortmund/costmap_prohibition_layer.git && \
#git clone https://github.com/SteveMacenski/spatio_temporal_voxel_layer.git -b noetic-devel && \
#git clone https://github.com/iralabdisco/ira_laser_tools.git && \
#git clone https://github.com/MoriKen254/timed_roslaunch.git && \
#mkdir summit_xl_sources && cd summit_xl_sources && \
#git clone https://github.com/RobotnikAutomation/rcomponent.git && \
#git clone https://github.com/RobotnikAutomation/robotnik_msgs.git && \
#git clone https://github.com/RobotnikAutomation/robotnik_sensors.git -b kinetic-devel && \
#git clone https://github.com/RobotnikAutomation/ros-system-monitor && \
#git clone https://github.com/RobotnikAutomation/summit_xls_ur5_common.git -b kinetic-multirobot-devel && \
#git clone https://github.com/RobotnikAutomation/summit_xl_common.git -b melodic-master 
# One of the two packages is needed only on robot controlling UR5 arm
# git clone https://github.com/RobotnikAutomation/ur_modern_driver.git # deprecated in favor of UniversalRobots/Universal_Robots_ROS_Driver.git 
# git clone https://github.com/UniversalRobots/Universal_Robots_ROS_Driver.git


#COPY /issues_solvers/pick_place_interface.py /opt/ros/"${ROS_DISTRO}"/lib/python3/dist-packages/moveit_python
# Add modified TB3 urdf with 359 scans instead of 360 for the Rplidar to make slam-toolbox work in sim
#COPY /issues_solvers/turtlebot3_burger.gazebo.xacro  /opt/ros/"${ROS_DISTRO}"/share/turtlebot3_description/urdf
#COPY /issues_solvers/turtlebot3_waffle.gazebo.xacro   /opt/ros/"${ROS_DISTRO}"/share/turtlebot3_description/urdf

# edit bashrc + workaround for this: https://github.com/SteveMacenski/spatio_temporal_voxel_layer/issues/167
RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc 
RUN  echo "export TURTLEBOT3_MODEL=burger" >> ~/.bashrc

#solve orbecc astra bug in xacro
#RUN sed -i 's/<sensor_orbbec_astra_gazebo/<xacro:sensor_orbbec_astra_gazebo/g' /home/$USER/catkin_ws/src/summit_xl_sources/robotnik_sensors/urdf/orbbec_astra.urdf.xacro

# configure repos for niryo
# RUN cd ~/catkin_ws/src/niryo_one_bringup && git checkout -b gazebo-simulator && git pull origin gazebo-simulator

#should solve the gpd_ros problem not finding opencv2
#COPY /issues_solvers/CMakeLists.txt  /home/"${USER}"/catkin_ws/src/gpd_ros

#RUN sudo pip3 install pyOpenSSL --upgrade
#RUN wget https://files.pythonhosted.org/packages/00/3f/ea5cfb789dddb327e6d2cf9377c36d9d8607af85530af0e7001165587ae7/pyOpenSSL-22.1.0-py3-none-any.whl
#RUN sudo pip3 install pyopenssl
#RUN sudo python3 -m easy_install pyOpenSSL-22.1.0-py3-none-any.whl
#RUN sudo pip3 install jsonpickle pyquaternion

# add gazebo models to decrease initial gazebo bringup time
#RUN mkdir -p ~/.gazebo
#ADD .gazebo /home/"${USER}"/.gazebo/
#RUN sudo chown $USER:$USER ~/.gazebo/models ; rm -rf /home/$USER/catkin_ws/src/robotiq_2finger_grippers/robotiq_modbus_rtu
#RUN cp -r ~/catkin_ws/src/icclab_summit_xl/worlds/models/marker* /home/"${user}"/.gazebo/models

# update dependencies
RUN sudo apt-get update && cd ~/colcon_ws && sudo rosdep init && \
rosdep update && rosdep install -ry --ignore-packages-from-source --from-paths src

# install ros-pcl AGAIN. No clue why it doesn't see it
#RUN sudo apt-get update && \
#    sudo apt-get install -y python3-pcl ros-${ROS_DISTRO}-pcl-ros wget vim ros-${ROS_DISTRO}-turtlebot3-bringup ros-${ROS_DISTRO}-rmw-cyclonedds-cpp 
#ros-${ROS_DISTRO}-moveit-python  doesn't work

# build workspace
RUN touch COLCON_IGNORE; cp COLCON_IGNORE ~/colcon_ws/src/kobuki_ros
RUN /bin/bash -c "source /opt/ros/${ROS_DISTRO}/setup.bash && cd colcon_ws && colcon build --symlink-install"

COPY env.sh /home/"${USER}"/env.sh
COPY cyclonedds.xml  /home/"${USER}"/cyclonedds.xml
#RUN echo "if [ -f "~/env.sh" ]; then source ~/env.sh; fi" >> ~/.bashrc

RUN /bin/bash -c "source /opt/ros/${ROS_DISTRO}/setup.bash"
# patch summit_xl old files and add unmerged PRs
#RUN bash -c "cd ~/catkin_ws/src/summit_xl_sources/summit_xl_common/summit_xl_description/urdf/wheels ; \
#    git checkout remotes/origin/kinetic-devel -- omni_wheel.urdf.xacro"

# add demo script
#COPY demo.sh  /home/"${USER}"/

