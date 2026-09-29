import os
from glob import glob

from setuptools import find_packages, setup

package_name = "camera_bridge"

setup(
    name=package_name,
    version="2.0.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", [f"resource/{package_name}"]),
        (f"share/{package_name}", ["package.xml"]),
        (os.path.join("share", package_name, "config"), glob("config/*.yaml")),
    ],
    install_requires=["setuptools", "edge_uploader"],
    zip_safe=True,
    maintainer="Attendance Platform Team",
    maintainer_email="eng@example.invalid",
    description="Phone camera access with stills, zoom, reconnect and heartbeat.",
    license="Apache-2.0",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "camera_bridge = camera_bridge.camera_node:main",
        ],
    },
)
