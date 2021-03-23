#!/usr/bin/env python3

import os
import setuptools

install_requires = [
    'empy',
    'pexpect',
    'packaging',
]

# docker API used to be in a package called `docker-py` before the 2.0 release
docker_package = 'docker'
try:
    import docker
except ImportError:
    # Docker is not yet installed, pick library based on platform
    # Use old name if platform has pre-2.0 version
    if os.path.isfile('/etc/os-release'):
        with open('/etc/os-release') as fin:
            content = fin.read()
        if 'xenial' in content:
            docker_package = 'docker-py'
else:
    # Docker is installed, pick library based on what we found
    ver = docker.__version__.split('.')
    if int(ver[0]) < 2:
        docker_package = 'docker-py'

install_requires.append(docker_package)

kwargs = {
    'name': 'groot_rocker',
    'version': '0.2.3',  # also update version.py
    'packages': ['groot_rocker'],
    'package_data': {'groot_rocker': ['templates/*.em']},
    'entry_points': {
        'console_scripts': [
            'groot-rocker = groot_rocker.cli:main',
            'detect_docker_image_os = groot_rocker.cli:detect_image_os'
        ],
        'groot_rocker.extensions': [
            'devices = groot_rocker.extensions:Devices',
            'dev_helpers = groot_rocker.extensions:DevHelpers',
            'env = groot_rocker.extensions:Environment',
            'git = groot_rocker.git_extension:Git',
            'home = groot_rocker.extensions:HomeDir',
            'name = groot_rocker.extensions:Name',
            'network = groot_rocker.extensions:Network',
            'nvidia = groot_rocker.nvidia_extension:Nvidia',
            'pulse = groot_rocker.extensions:PulseAudio',
            'ssh = groot_rocker.ssh_extension:Ssh',
            'user = groot_rocker.extensions:User',
            'x11 = groot_rocker.nvidia_extension:X11',
        ]
    },
    'author': 'Tully Foote',
    'author_email': 'tfoote@osrfoundation.org',
    'keywords': ['Docker'],
    'classifiers': [
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License'
    ],
    'description': 'A tool to run docker containers with customized extras',
    'long_description': 'A tool to run docker containers with customized extra added like nvidia gui support overlayed.',
    'license': 'Apache License 2.0',
    'python_requires': '>=3.0',

    'install_requires': install_requires,
    'url': 'https://github.com/stonier/groot_rocker'
}

setuptools.setup(**kwargs)
