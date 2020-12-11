FROM osrf/ros:foxy-desktop

ENV user=ros
ENV workspace=/home/ros

RUN apt -y update &&  apt -y upgrade && \ 
apt-get install -y wget unzip ros-foxy-rviz2 ros-foxy-rqt-image-view libconsole-bridge-dev ros-foxy-gazebo-ros-pkgs ros-foxy-ros-core ros-foxy-geometry2  && \
rm -rf /var/lib/apt/lists/*

# add ros user to container and make sudoer
RUN useradd -m -s /bin/bash -G video,plugdev  ${user} && \
echo "${user} ALL=(ALL) NOPASSWD: ALL" > "/etc/sudoers.d/${user}" && \
chmod 0440 "/etc/sudoers.d/${user}"

# add user to video group
RUN adduser ${user} video
RUN adduser ${user} plugdev

# Switch to user
USER "${user}"
# Switch to the workspace
WORKDIR ${workspace}

# edit bashrc
RUN echo "source /opt/ros/foxy/setup.bash" >> ~/.bashrc

CMD ["sleep", "90d"]
