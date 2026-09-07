#export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
#export CYCLONEDDS_URI=file:///${HOME}/cyclonedds.xml 
source ~/colcon_ws/install/setup.bash

# The container sees the node's CPUs (nproc -> 32 on the RAP nodes) but the pod is
# capped by a cgroup quota (limits.cpu: 16 in rap-lab-deployment-jazzy.yaml).
# Anything that sizes itself from nproc -- make, colcon, OpenMP inside PCL --
# therefore oversubscribes 2x and gets CFS-throttled, which is slower than simply
# using the right number of threads. Derive the real budget from the cgroup.
_rap_cpu_budget() {
  local rel quota period dir
  # Walk from this process's OWN cgroup up to the root, taking the first concrete
  # quota. Reading /sys/fs/cgroup/cpu.max directly is not enough: the RAP pod runs
  # privileged, so it sees the host cgroup hierarchy, whose root cpu.max is "max"
  # while the pod's real limit sits in its own subdirectory.
  if [ -e /sys/fs/cgroup/cgroup.controllers ] || [ -e /sys/fs/cgroup/cpu.max ]; then
    rel=$(awk -F: '$1=="0"{print $3; exit}' /proc/self/cgroup 2>/dev/null)
    dir="/sys/fs/cgroup${rel}"
    [ -d "$dir" ] || dir=/sys/fs/cgroup
    while : ; do
      if [ -r "$dir/cpu.max" ]; then
        read -r quota period < "$dir/cpu.max"
        if [ "$quota" != "max" ] && [ "${period:-0}" -gt 0 ] 2>/dev/null; then
          echo $(( quota / period )); return
        fi
      fi
      [ "$dir" = "/sys/fs/cgroup" ] && break
      dir=$(dirname "$dir")
    done
  fi
  # cgroup v1, same walk.
  rel=$(awk -F: '$2 ~ /(^|,)cpu(,|$)/ {print $3; exit}' /proc/self/cgroup 2>/dev/null)
  dir="/sys/fs/cgroup/cpu${rel}"
  [ -d "$dir" ] || dir=/sys/fs/cgroup/cpu
  while [ -d "$dir" ]; do
    if [ -r "$dir/cpu.cfs_quota_us" ] && [ -r "$dir/cpu.cfs_period_us" ]; then
      quota=$(cat "$dir/cpu.cfs_quota_us" 2>/dev/null)
      period=$(cat "$dir/cpu.cfs_period_us" 2>/dev/null)
      if [ "${quota:-0}" -gt 0 ] && [ "${period:-0}" -gt 0 ] 2>/dev/null; then
        echo $(( quota / period )); return
      fi
    fi
    [ "$dir" = "/sys/fs/cgroup/cpu" ] && break
    dir=$(dirname "$dir")
  done
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
