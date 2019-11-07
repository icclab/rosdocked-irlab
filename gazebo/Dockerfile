FROM robopaas/rosdocked-melodic

# Arguments
ENV user=ros
ARG uid
ENV home=/home/ros
ENV workspace=/home/ros/catkin_ws
ARG shell

# add ros user to container and make sudoer
RUN useradd -m -s /bin/bash -G video,plugdev  ${user} && \
echo "${user} ALL=(ALL) NOPASSWD: ALL" > "/etc/sudoers.d/${user}" && \
chmod 0440 "/etc/sudoers.d/${user}"

# add user to video group
RUN adduser ${user} video
RUN adduser ${user} plugdev

# Switch to user
USER "${user}"

# create catkin ws and clone projects
RUN mkdir -p ~/catkin_ws/src && cd ~/catkin_ws/src && /bin/bash -c "source /opt/ros/melodic/setup.bash && catkin_init_workspace" && \
git clone https://github.com/boschresearch/pcg_gazebo_pkgs.git && \
cd ~/catkin_ws && rosdep update && \
rosdep install --from-paths src --ignore-src --rosdistro=melodic -y -r && \
sudo apt-get update && sudo apt install -y libspatialindex-dev && \
cd ~/catkin_ws && /bin/bash -c "source /opt/ros/melodic/setup.bash && catkin_make"

# install required dependencies
RUN cd ~/catkin_ws/src/pcg_gazebo_pkgs/pcg_libraries && pip install --user -r requirements.txt

# install jupyter and add binaries to path
RUN pip install --user jupyter && echo "export PATH=$PATH:~/.local/bin" > ~/.bashrc

# This is required for sharing Xauthority
ENV QT_X11_NO_MITSHM=1
ENV CATKIN_TOPLEVEL_WS="${workspace}/devel"
# Switch to the workspace
WORKDIR ${workspace}
