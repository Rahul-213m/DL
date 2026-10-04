import os
from glob import glob

from setuptools import find_packages, setup

package_name = "edge_uploader"

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
    description="Durable, bounded, idempotent offline upload outbox.",
    license="Apache-2.0",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "edge_uploader = edge_uploader.uploader_node:main",
            "edge_requeue_failed = edge_uploader.requeue_failed:main",
        ],
    },
)
