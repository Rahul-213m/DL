from setuptools import find_packages
from setuptools import setup

setup(
    name='attendance_interfaces',
    version='2.0.0',
    packages=find_packages(
        include=('attendance_interfaces', 'attendance_interfaces.*')),
)
