from setuptools import setup, find_packages
import os
from glob import glob

package_name = 'attendance_robot'

setup(
    name=package_name,
    version='1.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        # ament index resource
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        # package.xml
        ('share/' + package_name, ['package.xml']),
        # launch files
        (os.path.join('share', package_name, 'launch'),
            glob('launch/*.py')),
        # URDF / Xacro files
        (os.path.join('share', package_name, 'urdf'),
            glob('urdf/*.xacro') + glob('urdf/*.urdf')),
        # config files
        (os.path.join('share', package_name, 'config'),
            glob('config/*.yaml')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Attendance Robot Team',
    maintainer_email='student@college.edu',
    description='ROS 2 Autonomous Classroom Attendance Camera Stand simulation',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            # Motor controller node
            'motor_controller = attendance_robot.motor_controller:main',
            # Camera interface node
            'camera_interface = attendance_robot.camera_interface:main',
            # Scan controller node (main orchestrator)
            'scan_controller = attendance_robot.scan_controller:main',
        ],
    },
)
