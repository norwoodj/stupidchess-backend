#!/usr/local/bin/python
from setuptools import setup, find_packages

setup(
    name="stupidchess",
    version="2024.7.0",
    packages=find_packages(),
    zip_safe=False,
    package_data={
        "stupidchess": ["templates/*.html", "*.json"],
    },
    install_requires=[
        "bcrypt",
        "flask",
        "flask-auth-utils",
        "flask-mongoengine",
        "healthcheck",
        "jconfigure",
        "nose",
    ],
)
