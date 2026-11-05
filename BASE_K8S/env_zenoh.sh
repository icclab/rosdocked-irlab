# Source for ROS 2 over Zenoh. Nodes use rmw_zenoh's default session config
# (connect to the local router on tcp/localhost:7447).
export RMW_IMPLEMENTATION=rmw_zenoh_cpp

# Start the local router. With ZENOH_ROUTER set by the deployment (tcp/<router>:<port>) it also
# connects to that router. The override is set for the router only: ZENOH_CONFIG_OVERRIDE
# applies to every node's session too, which would bypass the local router.
zenoh_router() {
  if [ -n "$ZENOH_ROUTER" ]; then
    ZENOH_CONFIG_OVERRIDE="${ZENOH_CONFIG_OVERRIDE:+$ZENOH_CONFIG_OVERRIDE;}connect/endpoints=[\"$ZENOH_ROUTER\"]" \
      ros2 run rmw_zenoh_cpp rmw_zenohd "$@"
  else
    ros2 run rmw_zenoh_cpp rmw_zenohd "$@"
  fi
}
