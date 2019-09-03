FROM robopaas/rosdocked-kinetic

# Arguments
ENV user=ros
ARG uid
ARG home
ARG workspace
ARG shell

# update ros.org keys
RUN apt-key del 421C365BD9FF1F717815A3895523BAEEB01FA116 && \
apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654

# add ros user to container and make sudoer
RUN useradd -m -s /bin/bash -G video,plugdev  ${user} && \
echo "${user} ALL=(ALL) NOPASSWD: ALL" > "/etc/sudoers.d/${user}" && \
chmod 0440 "/etc/sudoers.d/${user}"

# fix intel librealsense
RUN apt-get update
# dependencies needed by librealsense. `deb -i` will not resolve these
RUN apt-get install -y binutils cpp cpp-5 dkms fakeroot gcc gcc-5 kmod libasan2 libatomic1 libc-dev-bin libc6-dev libcc1-0 libcilkrts5 libfakeroot libgcc-5-dev libgmp10 libgomp1 libisl15 libitm1 liblsan0 libmpc3 libmpfr4 libmpx0 libquadmath0 libssl-dev libssl-doc libtsan0 libubsan0 libusb-1.0-0 libusb-1.0-0-dev libusb-1.0-doc linux-headers-4.4.0-159 linux-headers-4.4.0-159-generic linux-headers-generic linux-libc-dev make manpages manpages-dev menu patch zlib1g-dev
RUN apt-get install -y libssl-dev libssl-doc libusb-1.0-0 libusb-1.0-0-dev libusb-1.0-doc linux-headers-4.4.0-159 linux-headers-4.4.0-159-generic linux-headers-generic zlib1g-dev

# modify librealsense deb (unpack, replace script, repack)
RUN apt-get download ros-kinetic-librealsense
RUN dpkg-deb -R ros-kinetic-librealsense*.deb ros-rslib/
RUN wget https://gist.githubusercontent.com/dizz/404ef259a15e1410d692792da0c27a47/raw/3769e80a051b5f2ce2a08d4ee6f79c766724f495/postinst
RUN chmod +x postinst
RUN cp postinst ros-rslib/DEBIAN
RUN dpkg-deb -b ./ros-rslib/ ros-kinetic-librealsense_1.12.1-0xenial-20190830_icrlab_amd64.deb
# install container friendly libsense
RUN dpkg -i ros-kinetic-librealsense_1.12.1-0xenial-20190830_icrlab_amd64.deb
# lock from updates
RUN apt-mark hold ros-kinetic-librealsense


# Switch to user
USER "${user}"

# create catkin ws and clone projects
RUN mkdir -p ~/catkin_ws/src && cd ~/catkin_ws/ && /bin/bash -c "source /opt/ros/kinetic/setup.bash && catkin build" && \
cd src && \
git clone https://github.com/icclab/icclab_summit_xl.git && \
git clone --branch 1.0.2 https://github.com/JenniferBuehler/gazebo-pkgs.git && \
git clone --branch 1.0.0 https://github.com/JenniferBuehler/general-message-pkgs.git && \
git clone https://github.com/atenpas/gpg.git && \
git clone https://github.com/icclab/icclab_turtlebot.git -b kinetic && \
git clone https://github.com/icclab/irlab_point_cloud_filtering.git -b two_pcl_filtering && \
git clone https://github.com/icclab/laser_filters.git -b indigo-devel && \
git clone https://github.com/NiryoRobotics/niryo_one_ros.git && \
git clone --branch 2.2.1 https://github.com/intel-ros/realsense.git -b development && \
git clone https://github.com/atenpas/gpd.git -b forward && \
mkdir summit_xl_sources && cd summit_xl_sources && \
git clone https://github.com/RobotnikAutomation/rcomponent.git && \
git clone https://github.com/RobotnikAutomation/robotnik_msgs.git && \
git clone https://github.com/RobotnikAutomation/robotnik_sensors.git -b kinetic-multi-devel && \
git clone https://github.com/RobotnikAutomation/ros-system-monitor && \
git clone https://github.com/RobotnikAutomation/summit_xl_common.git -b kinetic-multirobot-devel && \
git clone https://github.com/RobotnikAutomation/summit_xls_ur5_common.git -b indigo-devel && \
git clone https://github.com/scanse/sweep-sdk.git && \
git clone https://github.com/RobotnikAutomation/ur_modern_driver.git

# add gazebo models to decrease initial gazebo bringup time
RUN mkdir -p ~/.gazebo
ADD .gazebo /home/"${user}"/.gazebo/

# patch gpd fwd
RUN cd ~/catkin_ws/src/gpd && \
wget https://patch-diff.githubusercontent.com/raw/atenpas/gpd/pull/63.patch && \
patch < 63.patch

RUN sudo apt-get install -y apt-utils

# update dependencies
RUN sudo apt-get update && cd ~/catkin_ws && \
rosdep update && rosdep install -ry --from-paths src

# Environment variables for noVNC
# Setup demo environment variables
ENV DEBIAN_FRONTEND=noninteractive \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8 \
    LC_ALL=C.UTF-8 \
    DISPLAY=:0.0 \
    DISPLAY_WIDTH=1024 \
    DISPLAY_HEIGHT=768 \
    RUN_FLUXBOX=yes

# Clone noVNC
RUN sudo git clone -b v1.1.0 https://github.com/novnc/noVNC.git /opt/novnc \
    && sudo rm -rf /opt/novnc/.git

# build workspace
RUN cd ~/catkin_ws && /bin/bash -c "source /opt/ros/kinetic/setup.bash && catkin build"

# update gazebo + x11vnc
RUN sudo sh -c 'echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable `lsb_release -cs` main" > /etc/apt/sources.list.d/gazebo-stable.list' && \
wget http://packages.osrfoundation.org/gazebo.key -O - | sudo apt-key add - && \
sudo apt-get update && sudo apt-get install -y gazebo7 x11vnc xvfb fluxbox

# edit bashrc
RUN echo "source catkin_ws/devel/setup.bash" >> ~/.bashrc

# fix for missing deps - there is prob a better way TODO: reeval this
RUN sudo apt-get install -y ros-kinetic-gazebo-ros-pkgs ros-kinetic-gazebo-ros-control ros-kinetic-ur-gazebo ros-kinetic-ur5-moveit-config ros-kinetic-ur-kinematics ros-kinetic-timed-roslaunch ros-kinetic-ira-laser-tools ros-kinetic-spatio-temporal-voxel-layer

# This is required for sharing Xauthority
ENV QT_X11_NO_MITSHM=1
ENV CATKIN_TOPLEVEL_WS="${workspace}/devel"
# Switch to the workspace
WORKDIR ${workspace}

# For noVNC and launching xvfb, x11vnc
EXPOSE 6080

CMD ["sudo", "supervisord", "-c", "/opt/novnc/supervisord/supervisord.conf"]
