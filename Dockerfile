FROM osrf/ros:foxy-desktop

RUN apt -y update &&  apt -y upgrade && \ 
apt-get install -y wget unzip ros-foxy-rviz2 ros-foxy-rqt-image-view libconsole-bridge-dev ros-foxy-gazebo-ros-pkgs ros-foxy-ros-core ros-foxy-geometry2  && \
rm -rf /var/lib/apt/lists/*

# fix missing libconsole_bridge.so.1.0
RUN cd /opt ; wget https://github.com/ros/console_bridge/archive/1.0.1.zip ; \
unzip 1.0.1.zip ; cd console_bridge-1.0.1 ; \
cmake -DCMAKE_INSTALL_PREFIX=/opt/ros/foxy/ ; make ; make install

ENV user=ros

# add ros user to container and make sudoer
RUN useradd -m -s /bin/bash -G video,plugdev  ${user} && \
echo "${user} ALL=(ALL) NOPASSWD: ALL" > "/etc/sudoers.d/${user}" && \
chmod 0440 "/etc/sudoers.d/${user}"

# add user to video group
RUN adduser ${user} video
RUN adduser ${user} plugdev

# Switch to user
USER "${user}"

# edit bashrc
#RUN echo "source opt/ros/foxy/setup.bash" >> ~/.bashrc


# This is required for sharing Xauthority
#ENV QT_X11_NO_MITSHM=1
#ENV CATKIN_TOPLEVEL_WS="${workspace}/devel"
# Switch to the workspace
#WORKDIR ${workspace}

# launch rviz2 package
CMD ["ros2", "run", "rviz2", "rviz2"]
