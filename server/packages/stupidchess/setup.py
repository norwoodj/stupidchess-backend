#!/usr/local/bin/python
from setuptools import setup, find_packages

setup(
    name="com.johnmalcolmnorwood.stupidchess",
    version="17.0914.0-dev",
    package_dir={"": "src"},
    packages=find_packages("src"),
    zip_safe=False,
    entry_points={
        "console_scripts": []
    },
    install_requires=[
        "bcrypt==3.1.0",
        "flask==0.11.1",
        "flask-mongoengine==0.8.2",
        "healthcheck==1.3.2",
        "jconfigure==17.0913.1",
        "nose==1.3.7",
        "com.johnmalcolmnorwood.auth==17.0914.0-dev",
    ],
)
