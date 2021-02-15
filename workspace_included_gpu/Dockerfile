#FROM osrf/ros:noetic-desktop-full
FROM nvidia/opengl:1.2-glvnd-runtime

ARG SOURCEFORGE=https://sourceforge.net/projects
ARG TURBOVNC_VERSION=2.1.2
ARG VIRTUALGL_VERSION=2.5.2
ARG LIBJPEG_VERSION=1.5.2
ARG WEBSOCKIFY_VERSION=0.8.0
ARG NOVNC_VERSION=1.0.0

ENV ROS_DISTRO=noetic
ENV DEBIAN_FRONTEND=noninteractive

# install min requirements
RUN apt update && apt-get upgrade -y && \
    apt install -y lsb-release gnupg sudo 

# set up ROS
RUN sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'&& \
    apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654

# install git and other needed libs including catkin build
RUN apt update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends git apt-utils ros-${ROS_DISTRO}-desktop-full \
    ros-${ROS_DISTRO}-pcl-ros python3-catkin-tools \
    python3-osrf-pycommon \
    curl wget vim less python lsof net-tools git htop \
    libxrender1 lubuntu-desktop xvfb xterm terminator zenity mesa-utils \
    x11-xkb-utils xauth 

# install turbovnc, virtualgl, noVNC
RUN cd /tmp && \
    curl -fsSL -O ${SOURCEFORGE}/turbovnc/files/${TURBOVNC_VERSION}/turbovnc_${TURBOVNC_VERSION}_amd64.deb \
        -O ${SOURCEFORGE}/libjpeg-turbo/files/${LIBJPEG_VERSION}/libjpeg-turbo-official_${LIBJPEG_VERSION}_amd64.deb \
        -O ${SOURCEFORGE}/virtualgl/files/${VIRTUALGL_VERSION}/virtualgl_${VIRTUALGL_VERSION}_amd64.deb \
        -O ${SOURCEFORGE}/virtualgl/files/${VIRTUALGL_VERSION}/virtualgl32_${VIRTUALGL_VERSION}_amd64.deb && \
    dpkg -i *.deb && \
    rm -f /tmp/*.deb && \
    sed -i 's/$host:/unix:/g' /opt/TurboVNC/bin/vncserver

ENV PATH ${PATH}:/opt/VirtualGL/bin:/opt/TurboVNC/bin

RUN apt install -y --no-install-recommends make cmake gcc

RUN curl -fsSL https://github.com/novnc/noVNC/archive/v${NOVNC_VERSION}.tar.gz | tar -xzf - -C /opt && \
    curl -fsSL https://github.com/novnc/websockify/archive/v${WEBSOCKIFY_VERSION}.tar.gz | tar -xzf - -C /opt && \
    mv /opt/noVNC-${NOVNC_VERSION} /opt/noVNC && \
    chmod -R a+w /opt/noVNC && \
    mv /opt/websockify-${WEBSOCKIFY_VERSION} /opt/websockify && \
    cd /opt/websockify && make && \
    cd /opt/noVNC/utils && \
    ln -s /opt/websockify

COPY xorg.conf /etc/X11/xorg.conf
COPY index.html /opt/noVNC/index.html

# Defeat screen locking and power management
# RUN mv /etc/xdg/autostart/light-locker.desktop /etc/xdg/autostart/light-locker.desktop_bak
# RUN mv /etc/xdg/autostart/xfce4-power-manager.desktop /etc/xdg/autostart/xfce4-power-manager.desktop_bak

# Expose whatever port NoVNC will serve from. In our case it will be 40001, see ./start_desktop.sh
EXPOSE 40001
ENV DISPLAY :1

ARG USER=ros

# add ros user to container and make sudoer
RUN useradd -m -s /bin/bash -G video,plugdev ${USER} && \
echo "${USER} ALL=(ALL) NOPASSWD: ALL" > "/etc/sudoers.d/${USER}" && \
chmod 0440 "/etc/sudoers.d/${USER}"

# Switch to user
USER "${USER}"

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
git clone https://github.com/ROBOTIS-GIT/turtlebot3_msgs.git && \
git clone https://github.com/ROBOTIS-GIT/turtlebot3.git && \
git clone https://github.com/ROBOTIS-GIT/turtlebot3_simulations.git && \
mkdir summit_xl_sources && cd summit_xl_sources && \
git clone https://github.com/RobotnikAutomation/rcomponent.git && \
git clone https://github.com/RobotnikAutomation/robotnik_msgs.git && \
git clone https://github.com/RobotnikAutomation/robotnik_sensors.git -b kinetic-devel && \
git clone https://github.com/RobotnikAutomation/ros-system-monitor && \
git clone https://github.com/RobotnikAutomation/summit_xl_common.git -b kinetic-multirobot-devel && \
git clone https://github.com/RobotnikAutomation/summit_xls_ur5_common.git -b kinetic-multirobot-devel && \
git clone https://github.com/RobotnikAutomation/ur_modern_driver.git

# configure repos for niryo
# RUN cd ~/catkin_ws/src/niryo_one_bringup && git checkout -b gazebo-simulator && git pull origin gazebo-simulator
# RUN cd ~/catkin_ws/src/irlab_point_cloud_filtering && git checkout -b dev && git pull origin dev

# add gazebo models to decrease initial gazebo bringup time
RUN mkdir -p ~/.gazebo
ADD .gazebo /home/"${USER}"/.gazebo/
RUN sudo chown ${USER}:${USER} ~/.gazebo/models ; rm -rf /home/ros/catkin_ws/src/robotiq_2finger_grippers/robotiq_modbus_rtu
RUN cp -r ~/catkin_ws/src/icclab_summit_xl/worlds/models/marker* /home/"${USER}"/.gazebo/models

# update dependencies
RUN sudo apt-get update && DEBIAN_FRONTEND=noninteractive sudo apt-get install -y python3-rosdep \ 
    ros-${ROS_DISTRO}-pcl-ros build-essential g++ python && \
    cd ~/catkin_ws && sudo rosdep init && \
    rosdep update && rosdep install -ry --ignore-packages-from-source --from-paths src 

# install ros-pcl AGAIN. No clue why it doesn't keep it
RUN sudo apt-get update && \
    sudo apt-get install -y ros-${ROS_DISTRO}-pcl-ros

# build workspace
RUN cd ~/catkin_ws && /bin/bash -c "source /opt/ros/${ROS_DISTRO}/setup.bash && catkin build"

# patch summit_xl old files and add unmerged PRs
RUN bash -c "cd ~/catkin_ws/src/summit_xl_sources/summit_xl_common/summit_xl_description/urdf/wheels ; \
    git checkout remotes/origin/kinetic-devel -- omni_wheel.urdf.xacro" #; \
#    bash -c "cd ~/catkin_ws/src/summit_xl_sources/robotnik_sensors; wget -O /tmp/11.patch https://patch-diff.githubusercontent.com/raw/RobotnikAutomation/robotnik_sensors/pull/11.patch; git apply /tmp/11.patch"

ENV CATKIN_TOPLEVEL_WS="/home/${USER}/catkin_ws"
# Switch to the workspace
WORKDIR /home/${USER}

# edit bashrc + workaround for this: https://github.com/SteveMacenski/spatio_temporal_voxel_layer/issues/167
RUN echo "source ~/catkin_ws/devel/setup.bash" >> ~/.bashrc 
#    echo "export LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libjemalloc.so.2" >> ~/.bashrc

# Defeat screen locking and power management
RUN sudo mv /etc/xdg/autostart/lxqt-xscreensaver-autostart.desktop /etc/xdg/autostart/lxqt-xscreensaver-autostart.desktop_bak && \
    sudo mv /etc/xdg/autostart/lxqt-powermanagement.desktop /etc/xdg/autostart/lxqt-powermanagement.desktop_bak && \
    sudo mv /etc/xdg/autostart/upg-notifier-autostart.desktop /etc/xdg/autostart/upg-notifier-autostart.desktop_bak

# Install desktop file for this user
RUN mkdir -p /home/${USER}/Desktop
COPY ./terminator.desktop /home/${USER}/Desktop/
RUN sudo chown ${USER}:${USER} /home/${USER}/Desktop/terminator.desktop
RUN mkdir -p /home/${USER}/.config/terminator
COPY ./terminator_config /home/${USER}/.config/terminator/config
COPY ./self.pem /home/${USER}/self.pem
RUN sudo chown ${USER}:${USER} /home/${USER}/self.pem
# Precede bash on all new terminator shells with vglrun so that 3d graphics apps will use the GPU
RUN sudo perl -pi -e 's/^Exec=terminator$/Exec=terminator -e "vglrun bash"/g' /usr/share/applications/terminator.desktop

# setup the X session started by turbovnc
RUN mkdir -p /home/${USER}/.vnc
COPY ./xstartup.turbovnc /home/${USER}/.vnc/xstartup.turbovnc
RUN sudo chown ${USER}:${USER} /home/${USER}/.vnc/xstartup.turbovnc

COPY start_desktop.sh /usr/local/bin/start_desktop.sh
CMD /usr/local/bin/start_desktop.sh

