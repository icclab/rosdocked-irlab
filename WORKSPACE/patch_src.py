"""Local fix-ups applied to the cloned repos in src/ by `pixi run setup`.

Each patch is idempotent and skips quietly once upstream has fixed the file, so
it is safe to re-run after `pixi run update`. Delete a patch here once its
upstream fix has landed.
"""
import pathlib
import sys

SRC = pathlib.Path(__file__).resolve().parent / "src"


def patch(rel_path, old, new, why):
    # Idempotent as long as `new` does not contain `old`.
    assert old not in new
    path = SRC / rel_path
    if not path.is_file():
        print(f"patch_src: {rel_path} not found, skipping")
        return
    text = path.read_text()
    if old not in text:
        return
    path.write_text(text.replace(old, new))
    print(f"patch_src: {rel_path}: {why}")


# Boost >= 1.89 (conda-forge ships 1.90) no longer has the boost_system stub, so
# this lookup fails at configure time. Nothing in the package uses Boost.
# Ubuntu Noble ships 1.83, which is why the Docker build does not hit it.
patch(
    "ros2_laser_scan_merger/CMakeLists.txt",
    "find_package(Boost REQUIRED COMPONENTS system)",
    "# Boost::system lookup removed by patch_src.py (unused; gone in Boost >= 1.89)",
    "dropped unused Boost::system lookup",
)

# RoboStack has no trac_ik build for Windows; KDL ships with MoveIt everywhere.
if sys.platform == "win32":
    patch(
        "icclab_summit_xl/icclab_summit_xl_move_it_config/config/kinematics.yaml",
        "trac_ik_kinematics_plugin/TRAC_IKKinematicsPlugin",
        "kdl_kinematics_plugin/KDLKinematicsPlugin",
        "arm IK switched from trac_ik to KDL (no trac_ik on Windows)",
    )
