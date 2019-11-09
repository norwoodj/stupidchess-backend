#!/usr/local/bin/python
from setuptools import setup, find_packages

setup(
    name="stupidchess",
    version="_VERSION",
    packages=find_packages(),
    zip_safe=False,
    package_data={
        "stupidchess": ["templates/*.html"],
    },
    entry_points={
        "console_scripts": [
            "setup_stupidchess_game=com.johnmalcolmnorwood.stupidchess.client.setup_stupidchess_game:main",
            "print_stupidchess_game=com.johnmalcolmnorwood.stupidchess.client.print_stupidchess_game:main",
        ],
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
