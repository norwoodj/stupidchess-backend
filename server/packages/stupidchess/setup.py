#!/usr/local/bin/python
from setuptools import setup, find_packages

setup(
    name="com.johnmalcolmnorwood.stupidchess",
    version="17.0920.0-dev",
    package_dir={"": "src"},
    packages=find_packages("src"),
    zip_safe=False,
    namespace_packages=["com", "com.johnmalcolmnorwood"],
    entry_points={
        "console_scripts": [
            "setup_stupidchess_game=com.johnmalcolmnorwood.stupidchess.client.setup_stupidchess_game:main",
        ],
    },
    install_requires=[
        "bcrypt",
        "flask",
        "flask-mongoengine",
        "healthcheck",
        "jconfigure",
        "nose",
        "com.johnmalcolmnorwood.auth",
    ],
)
