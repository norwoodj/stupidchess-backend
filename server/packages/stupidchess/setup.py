#!/usr/local/bin/python
from setuptools import setup, find_packages

setup(
    name='com.johnmalcolmnorwood.stupidchess',
    version='0.0.0-dev',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    zip_safe=False,
    entry_points={
        'console_scripts': []
    },
    install_requires=[
        'bcrypt==3.1.0',
        'flask==0.11.1',
        'flask-mongoengine==0.8.2',
        'nose==1.3.7',
        'com.johnmalcolmnorwood.auth==0.0.0-dev',
    ],
)
