#!/usr/bin/env python3
"""
manual_test.py
==============
Manual integration test script for the Attendance Camera Stand.

This script automates the manual test sequence described in the README.
Run it AFTER starting the nodes with:

  Terminal 1:
    cd ~/attendance_ros2_project
    source /opt/ros/humble/setup.bash
    source install/setup.bash
    ros2 launch attendance_robot display.launch.py use_rviz:=false

  Terminal 2:
    cd ~/attendance_ros2_project
    source /opt/ros/humble/setup.bash
    source install/setup.bash
    python3 src/attendance_robot/test/manual_test.py

Tests performed:
  1. Check all expected topics exist
  2. Check all expected services exist
  3. Send a manual set_target command and verify motor moves
  4. Start a scan session
  5. Monitor the scan sequence (angles + captures)
  6. Verify return to 0° after scan completes
  7. Test stop mid-scan
"""

import sys
import time
import subprocess


def run(cmd: str, timeout: int = 5) -> str:
    """Run a shell command, return stdout."""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=timeout
        )
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return '(timeout)'


def print_header(title: str):
    print(f'\n{"=" * 60}')
    print(f'  {title}')
    print(f'{"=" * 60}')


def check_topics():
    print_header('TEST 1: Check Topics')
    output = run('ros2 topic list', timeout=5)
    expected = [
        '/stand/current_angle',
        '/stand/target_angle',
        '/stand/set_target',
        '/stand/status',
        '/camera/status',
        '/camera/capture_count',
        '/scan/status',
        '/scan/current_index',
    ]
    all_ok = True
    for topic in expected:
        found = topic in output
        status = '✓' if found else '✗ MISSING'
        print(f'  {status}  {topic}')
        if not found:
            all_ok = False
    return all_ok


def check_services():
    print_header('TEST 2: Check Services')
    output = run('ros2 service list', timeout=5)
    expected = [
        '/scan/start',
        '/scan/stop',
        '/stand/stop',
        '/stand/reset',
        '/camera/capture',
    ]
    all_ok = True
    for srv in expected:
        found = srv in output
        status = '✓' if found else '✗ MISSING'
        print(f'  {status}  {srv}')
        if not found:
            all_ok = False
    return all_ok


def test_manual_angle_command():
    print_header('TEST 3: Manual Angle Command')
    print('  Publishing target angle 90° to /stand/set_target ...')
    run(
        "ros2 topic pub --once /stand/set_target std_msgs/msg/Float64 "
        "\"{'data': 90.0}\"",
        timeout=5
    )
    time.sleep(3)
    angle_str = run(
        'ros2 topic echo --once /stand/current_angle', timeout=5)
    print(f'  Current angle after command: {angle_str}')
    print('  Waiting for motor to settle at 90° ...')
    time.sleep(3)
    angle_str = run(
        'ros2 topic echo --once /stand/current_angle', timeout=5)
    print(f'  Current angle: {angle_str}')

    # Return to 0
    print('  Returning to 0° ...')
    run(
        "ros2 topic pub --once /stand/set_target std_msgs/msg/Float64 "
        "\"{'data': 0.0}\"",
        timeout=5
    )
    time.sleep(3)


def test_start_scan():
    print_header('TEST 4: Start Scan Session')
    print('  Calling /scan/start ...')
    output = run(
        'ros2 service call /scan/start std_srvs/srv/Trigger', timeout=10)
    print(f'  Response: {output}')
    print()
    print('  Monitoring /scan/status and /stand/current_angle for 45 seconds...')
    print('  (The default scan visits 0°→60°→120°→180°→240°→300° then returns to 0°)')
    print()

    for i in range(45):
        scan_status = run('ros2 topic echo --once /scan/status', timeout=2)
        motor_angle = run('ros2 topic echo --once /stand/current_angle', timeout=2)
        captures    = run('ros2 topic echo --once /camera/capture_count', timeout=2)
        print(
            f'  t={i:2d}s  scan={scan_status:<14}  '
            f'angle={motor_angle:<20}  captures={captures}'
        )
        time.sleep(1)


def test_angle_normalisation():
    print_header('TEST 5: Angle Normalisation (inline)')
    # Run purely in Python — no ROS 2 needed
    sys.path.insert(0, 'src/attendance_robot/attendance_robot')
    try:
        from motor_controller import normalise_angle
        cases = [
            (0,    0),
            (360,  0),
            (420,  60),
            (-60,  300),
            (-90,  270),
            (180,  180),
            (3600, 0),
        ]
        all_ok = True
        for inp, expected in cases:
            result = normalise_angle(float(inp))
            ok = abs(result - expected) < 0.001
            status = '✓' if ok else '✗'
            print(f'  {status}  normalise({inp:>5}°) = {result:.1f}°  '
                  f'(expected {expected}°)')
            if not ok:
                all_ok = False
        return all_ok
    except ImportError as e:
        print(f'  Could not import motor_controller: {e}')
        return False


def test_stop_scan():
    print_header('TEST 6: Stop Scan Mid-Session')
    # Start a new scan
    run('ros2 service call /scan/start std_srvs/srv/Trigger', timeout=5)
    print('  Scan started. Waiting 5s then stopping...')
    time.sleep(5)
    output = run('ros2 service call /scan/stop std_srvs/srv/Trigger', timeout=5)
    print(f'  Stop response: {output}')
    time.sleep(2)
    status = run('ros2 topic echo --once /scan/status', timeout=3)
    print(f'  Scan status after stop: {status}')


def main():
    print()
    print('╔══════════════════════════════════════════════════════════╗')
    print('║   Attendance Camera Stand — Manual Integration Tests    ║')
    print('╠══════════════════════════════════════════════════════════╣')
    print('║  Requires nodes running:                                 ║')
    print('║    ros2 launch attendance_robot display.launch.py        ║')
    print('║                         use_rviz:=false                  ║')
    print('╚══════════════════════════════════════════════════════════╝')
    print()

    # Allow time for nodes to start if just launched
    print('  Waiting 3s for nodes to initialise...')
    time.sleep(3)

    results = {}

    results['topics']   = check_topics()
    results['services'] = check_services()
    results['angles']   = test_angle_normalisation()

    test_manual_angle_command()
    test_start_scan()
    test_stop_scan()

    # Summary
    print_header('SUMMARY')
    for name, ok in results.items():
        status = '✓ PASS' if ok else '✗ FAIL'
        print(f'  {status}  {name}')

    print()
    print('Manual test sequence complete.')
    print('Check terminal 1 for node output logs.')


if __name__ == '__main__':
    main()
