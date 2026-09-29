#!/usr/bin/env bash
# Build and source the ROS 2 edge workspace with the CORRECT Python.
#
# WHY THIS SCRIPT EXISTS
# ----------------------
# Anaconda's Python 3.13 sits ahead of /usr/bin/python3 (3.12) on this machine.
# A plain `colcon build` therefore generates the ROS interfaces against 3.13,
# into install/<pkg>/lib/python3.13/, which the ROS runtime (3.12) cannot
# import. The build SUCCEEDS and then every message import fails at runtime:
#
#   UnsupportedTypeSupport: Could not import 'rosidl_typesupport_c'
#
# which is genuinely baffling because the build reported success.
#
# Stripping anaconda from PATH is NECESSARY BUT NOT SUFFICIENT: ROS's
# `python_cmake_module` scans a registry of known Python installations and
# still selects anaconda's. `-DPython3_EXECUTABLE` is what actually forces it.
# Both are done here.
#
# Verify after building:
#   ls install/attendance_interfaces/lib/ | grep python     # must say python3.12
#
# This script is idempotent and safe to run repeatedly.
set -eo pipefail

ROS_DISTRO="${ROS_DISTRO:-jazzy}"
WORKSPACE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BIN="${ROS_PYTHON:-/usr/bin/python3}"

if [[ ! -x "$PYTHON_BIN" ]]; then
  echo "error: $PYTHON_BIN not found. Set ROS_PYTHON to the ROS 2 Python." >&2
  exit 1
fi

echo "==> ROS distro : $ROS_DISTRO"
echo "==> workspace  : $WORKSPACE"
echo "==> python     : $PYTHON_BIN ($("$PYTHON_BIN" --version 2>&1))"

# Source ROS FIRST so its PYTHONPATH is set, then strip the conda entries.
# shellcheck disable=SC1091
set +u  # ROS setup.bash reads unset variables
source "/opt/ros/${ROS_DISTRO}/setup.bash"
set -u

CLEAN_PATH="$(printf '%s' "$PATH" | tr ':' '\n' \
  | grep -vE '/anaconda3|/miniconda3|/condaforge|/$(basename "$(dirname "$PYTHON_BIN")")/envs' \
  | paste -sd ':' -)"
CLEAN_PYTHONPATH="$(printf '%s' "${PYTHONPATH:-}" | tr ':' '\n' \
  | grep -vE '/anaconda3|/miniconda3|/condaforge' \
  | paste -sd ':' -)"

export PATH="$CLEAN_PATH"
export PYTHONPATH="$CLEAN_PYTHONPATH"
export PYTHON_EXECUTABLE="$PYTHON_BIN"
# CONDA_PYTHON_EXE is honoured by ROS's python_cmake_module and overrides PATH.
unset CONDA_PYTHON_EXE || true

echo "==> first python3 on PATH: $(command -v python3)"
cd "$WORKSPACE"

colcon build --symlink-install \
  --cmake-args "-DPython3_EXECUTABLE=$PYTHON_BIN" "-DPYTHON_EXECUTABLE=$PYTHON_BIN" "$@"

# Fail loudly here rather than at the first message import, which is where this
# otherwise shows up and looks like a corrupt install.
BUILT_PY="$(ls -d install/attendance_interfaces/lib/python3.* 2>/dev/null | head -1 | grep -oE 'python3\.[0-9]+' || true)"
WANT_PY="$("$PYTHON_BIN" -c 'import sys; print(f"python{sys.version_info.major}.{sys.version_info.minor}")')"
if [[ -n "$BUILT_PY" && "$BUILT_PY" != "$WANT_PY" ]]; then
  echo >&2
  echo "ERROR: interfaces were generated for $BUILT_PY but the ROS runtime is $WANT_PY." >&2
  echo "       Every message import will fail with UnsupportedTypeSupport." >&2
  echo "       Remove build/ install/ log/ and re-run this script." >&2
  exit 1
fi

echo
echo "==> build complete. To use the workspace:"
echo "      cd $WORKSPACE && source install/setup.bash"
