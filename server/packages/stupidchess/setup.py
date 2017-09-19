#!/usr/local/bin/python
from setuptools import setup, find_packages

setup(
    name="com.johnmalcolmnorwood.stupidchess",
    version="17.0919.0",
    package_dir={"": "src"},
    packages=find_packages("src"),
    zip_safe=False,
    namespace_packages=["com", "com.johnmalcolmnorwood"],
    entry_points={
        "console_scripts": [
            "create_stupidchess_set_up_game=com.johnmalcolmnorwood.stupidchess.client.create_stupidchess_set_up_game:main",
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
