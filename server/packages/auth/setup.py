#!/usr/local/bin/python
from setuptools import setup, find_packages

setup(
    name="com.johnmalcolmnorwood.auth",
    version="18.0123-dev",
    package_dir={"": "src"},
    packages=find_packages("src"),
    zip_safe=False,
    namespace_packages=["com", "com.johnmalcolmnorwood"],
    entry_points={},
    install_requires=[
        "flask",
        "flask-login",
    ],
)
