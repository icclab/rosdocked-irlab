#FROM ros:humble-ros-base
FROM osrf/ros:humble-desktop

# fix failing apt conf (TODO: remove when no longer an issue)
RUN rm /etc/apt/apt.conf.d/docker-clean 

ENV user=ros
ENV workspace=/home/ros
ENV ROS_DISTRO=humble

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
RUN echo "source /opt/ros/${ROS_DISTRO}/setup.bash" >> ~/.bashrc

#RUN sudo apt remove -m ros-humble-moveit-msgs
RUN sudo apt update
RUN /bin/bash -c "mkdir -p ws_moveit/src && cd ws_moveit/src && \
    rosdep update && \
    git clone https://github.com/stooppas/moveit2 && \
    git clone https://github.com/stooppas/moveit_msgs -b ros2 && \
    vcs import < moveit2/moveit2.repos && \
    rosdep install -r --from-paths . --ignore-src --rosdistro $ROS_DISTRO -y && \
    cd .. && \
    colcon build --event-handlers desktop_notification- status- --executor sequential --cmake-args -DCMAKE_BUILD_TYPE=Release"

CMD ["sleep", "90d"]