"""Integration test harness for the ROS edge.

These tests are here because of a specific, repeatedly demonstrated fact: in
W5, every single integration bug lived in the ROS WIRING, and not one of them
was caught by a unit test. The servo package shipped with 55 passing tests and
could not move the mechanism once, because the tests exercised the driver and
not the action server.

So these tests do the things unit tests structurally cannot:

* start the REAL nodes as real processes,
* talk to them over real DDS with a real client,
* kill them, stall them and cancel them,
* and assert the thing an operator would actually see.

HOW THE ENVIRONMENT IS BUILT
The tests run in-process as rclpy clients, so the workspace's install tree must
be on the environment. Rather than requiring the caller to have sourced
setup.bash (which is easy to forget and impossible in CI), the environment is
reconstructed once per session by asking bash to source it and print the
result. That is the same thing a shell would do, minus the human.

NO FIXED SLEEPS
Every wait is a poll for a condition with a deadline. A test that sleeps "long
enough" is a test that fails on a loaded CI machine and passes on a laptop, and
it is worse than no test because it looks like coverage.

DOMAIN IDS
Each session gets its own ROS_DOMAIN_ID, derived from the PID, so concurrent
sessions -- a local run and a CI run, or two developers -- cannot discover each
other's nodes. Tests inherit it, so a stray node from another test session
cannot make a wait succeed early.
"""

from __future__ import annotations

import contextlib
import os
import shutil
import signal
import subprocess
import time
from pathlib import Path

import pytest

# conftest.py is ros_ws/tests/integration/conftest.py, so parents[2] is ros_ws.
ROS_WS = Path(__file__).resolve().parents[2]
ROS_DISTRO = os.environ.get("ROS_DISTRO", "jazzy")
ROS_SETUP = Path("/opt/ros") / ROS_DISTRO / "setup.bash"
WS_SETUP = ROS_WS / "install" / "setup.bash"

#: Long enough for four Python nodes to import cv2/numpy and build their
#: action clients, short enough that a hung launch fails the test in
#: reasonable time.
LAUNCH_READY_TIMEOUT_S = 90.0
#: Per-condition deadline for "the system reached state X".
CONDITION_TIMEOUT_S = 60.0


def _build_workspace_env() -> dict[str, str]:
    """Return an environment with the ROS and workspace overlays applied.

    Raises:
        RuntimeError: If the workspace has not been built, with the command to
            fix it. Failing here with instructions beats a baffling
            ModuleNotFoundError twenty seconds later.
    """
    if not WS_SETUP.exists():
        raise RuntimeError(
            f"{WS_SETUP} does not exist. Build the workspace first:\n"
            f"    {ROS_WS / 'build.sh'}\n"
            "(It must be build.sh, not a bare colcon build -- see the note on "
            "the ROS system Python in docs/PROGRESS.md.)"
        )
    if not ROS_SETUP.exists():
        raise RuntimeError(f"{ROS_SETUP} not found; is ROS 2 {ROS_DISTRO} installed?")

    # `env -0` so values containing newlines survive; python-version managers
    # put multi-line values in LD_LIBRARY_PATH and PYTHONPATH.
    script = f"source '{ROS_SETUP}' && source '{WS_SETUP}' && env -0"
    result = subprocess.run(
        ["bash", "-c", script], capture_output=True, check=True, env={**os.environ, "HOME": str(Path.home())}
    )
    env = {}
    for chunk in result.stdout.split(b"\0"):
        if not chunk:
            continue
        key, _, value = chunk.decode().partition("=")
        env[key] = value
    return env


def wait_for_node(visible: set[str], name: str, timeout_s: float) -> bool:
    """Wait for a node name to appear among the visible nodes."""
    return wait_for(
        lambda: name in visible(),
        timeout_s=timeout_s,
        what=f"the {name} node to appear",
    )


@pytest.fixture(scope="session")
def ros_env() -> dict[str, str]:
    """The overlay environment, built once per session."""
    return _build_workspace_env()


@pytest.fixture(scope="session")
def domain_id() -> int:
    """A ROS_DOMAIN_ID private to this session.

    Derived from the PID so two concurrent pytest sessions -- two shells, or a
    local run alongside CI -- do not discover each other's nodes. Without
    isolation, a leftover node from a previous run makes a "wait until the
    sweep server exists" check pass against the WRONG process.
    """
    return 60 + (os.getpid() % 60)


@pytest.fixture(scope="session")
def session_env(ros_env: dict[str, str], domain_id: int) -> dict[str, str]:
    """Overlay environment plus this session's domain id."""
    return {**ros_env, "ROS_DOMAIN_ID": str(domain_id), "RCUTILS_LOGGING_BUFFERED_STREAM": "0"}


class EdgeSystem:
    """A running set of edge nodes, managed as a test fixture.

    Owns the process group, the data root and the generated config, and knows
    how to ask the running system questions without fixed sleeps.
    """

    def __init__(self, env: dict[str, str], data_root: Path, log_path: Path) -> None:
        self.env = env
        self.data_root = data_root
        self.log_path = log_path
        self.process: subprocess.Popen | None = None
        self._log_handle = None
        self._extra_processes: list[subprocess.Popen] = []
        #: Whether the most recent kill_node() actually signalled a process.
        #: A retry loop uses this to tell "already dead" from "still alive".
        self._last_kill_matched = False
        self.ros2 = shutil.which("ros2", path=env.get("PATH", os.environ.get("PATH", "")))

    # -- lifecycle ------------------------------------------------------
    def start(self, *, extra_args: list[str] | None = None) -> EdgeSystem:
        """Launch the edge in simulated mode.

        ``start_new_session`` puts the children in their own process group, so
        ``stop`` can kill the whole tree. Without it, killing the launcher
        orphans four Python processes that keep answering ROS calls, and the
        NEXT test in the session talks to a ghost.
        """
        config = self._write_config()
        self._log_handle = self.log_path.open("w", encoding="utf-8")
        command = [
            self.ros2 or "ros2",
            "launch",
            "attendance_bringup",
            "edge.launch.py",
            "mode:=simulated",
            f"config_file:={config}",
            *(extra_args or []),
        ]
        self.process = subprocess.Popen(
            command,
            stdout=self._log_handle,
            stderr=subprocess.STDOUT,
            env=self.env,
            cwd=str(ROS_WS),
            start_new_session=True,
        )
        return self

    def _write_config(self) -> Path:
        """Generate a per-test config with a private data root.

        The shipped simulated profile points at a shared /tmp path. Tests must
        not: two tests sharing an outbox cannot assert anything about how many
        captures were written, which is exactly the thing being tested.
        """
        source = ROS_WS / "install" / "attendance_bringup" / "share" / "attendance_bringup" / "config"
        text = (source / "edge_simulated.yaml").read_text(encoding="utf-8")
        target = self.data_root.parent / f"edge_{os.getpid()}_{abs(hash(self.data_root)) % 10_000}.yaml"
        target.write_text(text.replace("/tmp/attendance-simulated", str(self.data_root)), encoding="utf-8")
        self.config_path = target
        return target

    def stop(self, *, timeout_s: float = 15.0) -> None:
        """Stop every node, escalating to SIGKILL if they will not go."""
        if self.process is None:
            return
        if self.process.poll() is None:
            with contextlib.suppress(ProcessLookupError):
                os.killpg(os.getpgid(self.process.pid), signal.SIGINT)
            try:
                self.process.wait(timeout=timeout_s)
            except subprocess.TimeoutExpired:
                with contextlib.suppress(ProcessLookupError):
                    os.killpg(os.getpgid(self.process.pid), signal.SIGKILL)
                self.process.wait(timeout=timeout_s)
        for process in self._extra_processes:
            if process.poll() is None:
                with contextlib.suppress(ProcessLookupError, ProcessLookupError):
                    os.killpg(os.getpgid(process.pid), signal.SIGKILL)
        self._extra_processes.clear()
        if self._log_handle is not None:
            self._log_handle.close()
            self._log_handle = None

    def kill_node(self, package: str) -> None:
        """Kill one node by its install path, simulating a hardware loss.

        SIGKILL, not SIGINT: a phone that loses power does not run a shutdown
        handler, and a graceful shutdown would exercise a code path that a
        real failure never reaches.
        """
        targets = self._executables(package)
        if not targets:
            raise AssertionError(
                f"no installed executable found for {package!r}; kill_node() would "
                "have reported success while killing nothing"
            )
        killed = 0
        for target in targets:
            for pid_dir in Path("/proc").iterdir():
                if not pid_dir.name.isdigit():
                    continue
                try:
                    cmdline = (pid_dir / "cmdline").read_bytes().decode(errors="replace")
                except (OSError, PermissionError):
                    continue
                if str(target) in cmdline and "ros2" not in cmdline.split(target.name)[0]:
                    with contextlib.suppress(ProcessLookupError):
                        os.kill(int(pid_dir.name), signal.SIGKILL)
                        killed += 1
        if not killed:
            # Not an error: the node may already be dead, and a caller killing
            # twice is a legitimate retry. The caller decides whether an absent
            # process is acceptable -- see kill_node_until_gone, which raises
            # when the node is STILL there afterwards, because then the fault
            # under test never happened.
            self._last_kill_matched = False
        else:
            self._last_kill_matched = True

    def _executables(self, package: str) -> list[Path]:
        """Every installed executable for a package, across all install prefixes.

        Not just AMENT_PREFIX_PATH[0]: that is ONE package's install prefix, in
        an arbitrary order, so looking for camera_bridge's executable there
        silently finds nothing. kill_node() then reported success while
        killing nothing, and every fault-injection test built on it was
        testing nothing at all.
        """
        found: list[Path] = []
        for prefix in self.env.get("AMENT_PREFIX_PATH", "").split(os.pathsep):
            if not prefix:
                continue
            candidate = Path(prefix) / "lib" / package / package
            if candidate.exists():
                found.append(candidate)
        # Also check the workspace install tree, which is where a colcon build
        # with --symlink-install actually puts them.
        ws_install = ROS_WS / "install"
        if ws_install.is_dir():
            for prefix in sorted(ws_install.iterdir()):
                candidate = prefix / "lib" / package / package
                if candidate.exists() and candidate not in found:
                    found.append(candidate)
        return found

    def restart_node(self, package: str, *, extra_args: list[str] | None = None) -> None:
        """Relaunch a node that kill_node() removed.

        Launched as its own `ros2 run`, with the same params file, because
        that is what a systemd unit or a container restart actually does: it
        starts one process, not a second copy of the entire system. Calling
        start() here would launch a SECOND complete edge alongside the first,
        and then two nodes answer the same service -- which is a far more
        confusing thing to debug than the fault under test.
        """
        handle = self._log_handle or self.log_path.open("a", encoding="utf-8")
        process = subprocess.Popen(
            [
                self.ros2 or "ros2",
                "run",
                package,
                package,
                "--ros-args",
                "--params-file",
                str(self.config_path),
                *(extra_args or []),
            ],
            stdout=handle,
            stderr=subprocess.STDOUT,
            env=self.env,
            cwd=str(ROS_WS),
            start_new_session=True,
        )
        self._extra_processes.append(process)
        wait_for_node(self.nodes, package, timeout_s=90.0)

    def outbox_dir(self) -> Path:
        """Where the uploader actually writes, read from the live config.

        Guessing this path in a test is how a durability test ends up
        asserting on an empty directory that was never used.
        """
        import re

        text = Path(self.config_path).read_text(encoding="utf-8")
        match = re.search(r"data_root:\s*[\"']?([^\"'\n]+)", text)
        if not match:
            raise AssertionError(f"no data_root in {self.config_path}")
        root = Path(match.group(1).strip())
        # The uploader namespaces its queue under the tenant, so search rather
        # than guess the second level.
        for candidate in [root, *root.glob("*/outbox"), *root.glob("outbox")]:
            if candidate.is_dir():
                return candidate
        return root

    def journal_path(self) -> Path:
        """The outbox journal. Named in outbox.py, and asserted to exist."""
        return self.outbox_dir() / "outbox.jsonl"

    # -- observation ----------------------------------------------------
    def log(self) -> str:
        """The captured launch output."""
        if self.log_path.exists():
            return self.log_path.read_text(encoding="utf-8", errors="replace")
        return ""

    def died_nodes(self) -> list[str]:
        """Which launched processes died. Must be empty in a healthy run."""
        died = []
        for line in self.log().splitlines():
            if "process has died" in line:
                died.append(line.split("[")[1].split("]")[0] if "[" in line else line)
        return died

    def run_ros2(self, *args: str, timeout_s: float = 30.0) -> str:
        """Run a `ros2` CLI command against the running system."""
        result = subprocess.run(
            [self.ros2 or "ros2", *args],
            capture_output=True,
            text=True,
            env=self.env,
            timeout=timeout_s,
            cwd=str(ROS_WS),
            check=False,
        )
        if result.returncode != 0:
            raise AssertionError(f"ros2 {' '.join(args)} failed ({result.returncode}):\n{result.stderr}")
        return result.stdout

    def nodes(self) -> set[str]:
        """Currently visible node names, WITHOUT the leading slash.

        Normalised deliberately. `ros2 node list` prints `/servo_controller`,
        while the launch file, the config files and every test refers to the
        node as `servo_controller`. Comparing the two forms silently yields
        False for every node, so a "is it running?" check always answers no --
        which reads as a product that will not start rather than as a
        string-prefix bug in the harness.
        """
        return {
            line.strip().lstrip("/") for line in self.run_ros2("node", "list").splitlines() if line.strip()
        }

    def topics(self) -> dict[str, list[str]]:
        """Topic name -> interface types."""
        result: dict[str, list[str]] = {}
        for line in self.run_ros2("topic", "list", "-t").splitlines():
            if "[" not in line:
                continue
            name, _, types = line.partition("[")
            result[name.strip()] = [t.strip() for t in types.rstrip("]").split(",")]
        return result

    def services(self) -> dict[str, list[str]]:
        """Service name -> interface types."""
        result: dict[str, list[str]] = {}
        for line in self.run_ros2("service", "list", "-t").splitlines():
            if "[" not in line:
                continue
            name, _, types = line.partition("[")
            result[name.strip()] = [t.strip() for t in types.rstrip("]").split(",")]
        return result

    def actions(self) -> dict[str, list[str]]:
        """Action name -> interface types."""
        result: dict[str, list[str]] = {}
        for line in self.run_ros2("action", "list", "-t").splitlines():
            if "[" not in line:
                continue
            name, _, types = line.partition("[")
            result[name.strip()] = [t.strip() for t in types.rstrip("]").split(",")]
        return result


def wait_for(
    predicate, timeout_s: float = CONDITION_TIMEOUT_S, interval_s: float = 0.25, what: str = "condition"
):
    """Poll ``predicate`` until it is true, or fail with a useful message.

    Polling rather than sleeping: a sleep long enough on a fast machine is a
    race on a loaded one, and a retry loop hides the flakiness instead of
    fixing it.
    """
    deadline = time.monotonic() + timeout_s
    last = None
    while time.monotonic() < deadline:
        last = predicate()
        if last:
            return last
        time.sleep(interval_s)
    raise AssertionError(f"timed out after {timeout_s:.0f}s waiting for {what} (last value: {last!r})")


@pytest.fixture(scope="module")
def edge_system(session_env, tmp_path_factory) -> EdgeSystem:
    """One running edge system per test module.

    Module scope: starting four Python nodes takes ~10 s, and the point of
    these tests is the system's behaviour, not per-test isolation of the
    process set. Tests that KILL a node ask for their own system via
    ``destructive_edge_system``.
    """
    data_root = tmp_path_factory.mktemp("edge_data") / "outbox"
    log_path = tmp_path_factory.mktemp("edge_logs") / "launch.log"
    system = EdgeSystem(session_env, data_root, log_path)
    system.start()
    wait_for(
        lambda: len(system.nodes()) >= 4,
        timeout_s=LAUNCH_READY_TIMEOUT_S,
        what="all four edge nodes to appear",
    )
    yield system
    system.stop()


#: Every node the simulated edge runs. Used to repair the system between
#: fault-injection tests, which damage it on purpose.
REQUIRED_NODES = ("servo_controller", "camera_bridge", "scan_planner", "edge_uploader")


@pytest.fixture
def repaired_edge_system(destructive_edge_system) -> EdgeSystem:
    """A destructive system with every node running, whatever the last test left.

    Fault injection is destructive by definition, so a module-scoped fixture
    hands each test the previous test's wreckage. Without this repair, the
    second test to kill the uploader fails with "the node was not running" --
    which reads like a product bug and is really a test-isolation bug. That
    distinction matters: the next person would otherwise go and "fix" the
    product to satisfy a test that was never testing anything.
    """
    edge = destructive_edge_system
    for name in REQUIRED_NODES:
        if name not in edge.nodes():
            edge.restart_node(name)
    return edge


@pytest.fixture(scope="module")
def destructive_edge_system(session_env, tmp_path_factory) -> EdgeSystem:
    """A separate running system for tests that kill or corrupt nodes."""
    data_root = tmp_path_factory.mktemp("destructive_data") / "outbox"
    log_path = tmp_path_factory.mktemp("destructive_logs") / "launch.log"
    system = EdgeSystem(session_env, data_root, log_path)
    system.start()
    wait_for(
        lambda: len(system.nodes()) >= 4,
        timeout_s=LAUNCH_READY_TIMEOUT_S,
        what="all four edge nodes to appear",
    )
    yield system
    system.stop()


class RosHarness:
    """An in-process rclpy client for talking to the running system.

    Note that `wait_for_service` is a method on a **Client**, not on a Node --
    an early version of this harness called `node.wait_for_service` and failed
    every test with an AttributeError, which is a good reminder to check the
    API rather than assume it.
    """

    def __init__(self, node) -> None:
        self.node = node

    def client(self, srv_type, name: str, timeout_s: float = CONDITION_TIMEOUT_S):
        """Create a service client and wait for it to be discovered."""
        client = self.node.create_client(srv_type, name)
        assert wait_for(lambda: client.service_is_ready(), timeout_s, what=f"service {name}"), (
            f"service {name} never became ready"
        )
        return client

    def action_client(self, action_type, name: str):
        """Create an action client and wait for its server to appear."""
        from rclpy.action import ActionClient

        client = ActionClient(self.node, action_type, name)
        assert wait_for(
            lambda: client.server_is_ready(), CONDITION_TIMEOUT_S, what=f"action server {name}"
        ), f"action server {name} never became ready"
        return client

    def wait_until(self, predicate, timeout_s: float = CONDITION_TIMEOUT_S, what: str = "condition"):
        """Spin this node until a predicate is true.

        Subscriptions only deliver while the node is spinning, so a test that
        subscribes and then asserts on a list will always see it empty unless
        something spins in between. This is that something -- it is the
        difference between a subscription-based test that works and one that
        times out for no visible reason.
        """
        import time as _time

        import rclpy

        deadline = _time.monotonic() + timeout_s
        while _time.monotonic() < deadline:
            rclpy.spin_once(self.node, timeout_sec=0.1)
            if predicate():
                return True
        raise AssertionError(
            f"timed out after {timeout_s:.0f}s waiting for {what} "
            "(the node was spinning throughout, so nothing arrived)"
        )

    def spin_until(self, future, timeout_s: float = CONDITION_TIMEOUT_S):
        """Spin this test node until a future resolves, or fail loudly."""
        import rclpy

        rclpy.spin_until_future_complete(self.node, future, timeout_sec=timeout_s)
        assert future.done(), f"future did not complete within {timeout_s:.0f}s"
        return future.result()

    def call(self, client, request, timeout_s: float = CONDITION_TIMEOUT_S):
        """Call a service and return the response."""
        return self.spin_until(client.call_async(request), timeout_s)

    def goal_and_result(
        self, client, goal, *, accept_timeout_s: float = 20.0, result_timeout_s: float = CONDITION_TIMEOUT_S
    ):
        """Send a goal, assert it was accepted, and return the result wrapper.

        Returns the `GetResult_Response`, so the caller can assert on BOTH the
        status byte and the result message -- the pair that this project has
        repeatedly got wrong in one half or the other.
        """
        handle = self.spin_until(client.send_goal_async(goal), accept_timeout_s)
        assert handle.accepted, "the goal was rejected"
        return self.spin_until(handle.get_result_async(), result_timeout_s)


@pytest.fixture
def ros_node(session_env):
    """An in-process rclpy client, created and destroyed per test.

    Per-test, not per-module: rclpy keeps global state (the default context,
    signal handlers) and two live contexts in one process reliably produce a
    hang that looks like a product bug.
    """
    import rclpy

    for key, value in session_env.items():
        os.environ[key] = value

    if not rclpy.ok():
        rclpy.init()
    node = rclpy.create_node("integration_test_client")
    try:
        yield RosHarness(node)
    finally:
        node.destroy_node()


def pytest_report_header(config) -> str:
    """Say which domain these tests own, so a failure is diagnosable."""
    return f"integration domain: ROS_DOMAIN_ID={60 + (os.getpid() % 60)}"
