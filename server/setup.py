#!/usr/local/bin/python
from setuptools import setup, find_packages

setup(
    name='com.johnmalcomnorwood.stupidchess',
    version='0.0.0.dev0',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    zip_safe=False,
    entry_points={
        'console_scripts': []
    },
    install_requires=[
        'flask-mongoengine',
        'nose',
    ],
)
