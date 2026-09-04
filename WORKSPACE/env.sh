#export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
#export CYCLONEDDS_URI=file:///${HOME}/cyclonedds.xml 
source ~/colcon_ws/install/setup.bash

# The container sees the node's CPUs (nproc -> 32 on the RAP nodes) but the pod is
# capped by a cgroup quota (limits.cpu: 16 in rap-lab-deployment-jazzy.yaml).
# Anything that sizes itself from nproc -- make, colcon, OpenMP inside PCL --
# therefore oversubscribes 2x and gets CFS-throttled, which is slower than simply
# using the right number of threads. Derive the real budget from the cgroup.
_rap_cpu_budget() {
  local quota period
  if [ -r /sys/fs/cgroup/cpu.max ]; then                      # cgroup v2
    read -r quota period < /sys/fs/cgroup/cpu.max
    if [ "$quota" != "max" ] && [ "${period:-0}" -gt 0 ] 2>/dev/null; then
      echo $(( quota / period )); return
    fi
  elif [ -r /sys/fs/cgroup/cpu/cpu.cfs_quota_us ]; then       # cgroup v1
    quota=$(cat /sys/fs/cgroup/cpu/cpu.cfs_quota_us 2>/dev/null)
    period=$(cat /sys/fs/cgroup/cpu/cpu.cfs_period_us 2>/dev/null)
    if [ "${quota:-0}" -gt 0 ] && [ "${period:-0}" -gt 0 ] 2>/dev/null; then
      echo $(( quota / period )); return
    fi
  fi
  nproc                                                        # not capped
}
RAP_CPUS=$(_rap_cpu_budget)
[ "${RAP_CPUS:-0}" -ge 1 ] 2>/dev/null || RAP_CPUS=$(nproc)
export RAP_CPUS
# colcon runs several packages at once, each running its own make, so the totals
# multiply: parallel-workers (2, set in ~/.colcon/defaults.yaml) x MAKEFLAGS jobs
# should land on the budget rather than blow through it.
_rap_jobs=$(( RAP_CPUS / 2 )); [ "$_rap_jobs" -ge 1 ] || _rap_jobs=1
export MAKEFLAGS="-j${_rap_jobs}"
# Runtime OpenMP (PCL, and anything else that grabs every core it can see).
export OMP_NUM_THREADS="${RAP_CPUS}"

echo "** ROS2 $ROS_DISTRO initialized with $RMW_IMPLEMENTATION**"
if [ "${RAP_CPUS}" != "$(nproc)" ]; then
  echo "** ${RAP_CPUS} CPUs available to this pod (node has $(nproc)); build and OpenMP parallelism capped accordingly **"
fi
#source install/setup.bash
