import os
from glob import glob

from setuptools import find_packages, setup

package_name = "scan_planner"

setup(
    name=package_name,
    version="2.0.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", [f"resource/{package_name}"]),
        (f"share/{package_name}", ["package.xml"]),
        (os.path.join("share", package_name, "config"), glob("config/*.yaml")),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Attendance Platform Team",
    maintainer_email="eng@example.invalid",
    description="Room-aware scan planning with zoom strategy and a time budget.",
    license="Apache-2.0",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "scan_planner = scan_planner.scan_node:main",
            "show_face_sizes = scan_planner.show_face_sizes:main",
        ],
    },
)
