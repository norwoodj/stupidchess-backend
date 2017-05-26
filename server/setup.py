#!/usr/local/bin/python
from setuptools import setup, find_packages

setup(
    name='com.johnmalcomnorwood.stupidchess',
    version='0.0.0-dev',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'create_sc_set_up_game=com.johnmalcolmnorwood.stupidchess.scripts:main',
        ],
    },
    install_requires=[
        'flask-mongoengine',
        'nose',
    ],
)
