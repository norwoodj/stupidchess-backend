#!/usr/local/bin/python
from setuptools import setup, find_packages

setup(
    name="com.johnmalcolmnorwood.auth",
    version="17.0906.0-dev",
    package_dir={"": "src"},
    packages=find_packages("src"),
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "create_sc_set_up_game=com.johnmalcolmnorwood.stupidchess.scripts:main",
        ],
    },
    install_requires=[
        "flask==0.11.1",
        "flask-login==0.4.0",
    ],
)
