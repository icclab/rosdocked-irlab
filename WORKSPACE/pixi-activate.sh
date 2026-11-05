# Sourced by pixi on activation (pixi shell / pixi run). Overlays the colcon
# workspace on top of the ROS install in .pixi/ once it has been built.
if [ -f "$PIXI_PROJECT_ROOT/install/local_setup.sh" ]; then
  . "$PIXI_PROJECT_ROOT/install/local_setup.sh"
fi
# Gazebo models shipped in this directory (cafe_table, markers, ...).
export GZ_SIM_RESOURCE_PATH="$PIXI_PROJECT_ROOT/.gazebo/models${GZ_SIM_RESOURCE_PATH:+:$GZ_SIM_RESOURCE_PATH}"
