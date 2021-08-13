#!/usr/bin/env python3

import os
import setuptools

install_requires = [
    'empy',
    'pexpect',
    'packaging',
    'pyyaml',
    'six',  # workaround for missing dependency transitive to docker
]


extras_require = {
    'tests': ['codecov', 'coverage', 'nose', 'pytest'],
    'packaging': ['stdeb', 'twine']
}

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
    'version': '0.3.4',
    'packages': ['groot_rocker'],
    'package_data': {'groot_rocker': ['templates/*.em']},
    'entry_points': {
        'console_scripts': [
            'groot-rocker = groot_rocker.cli:main',
            'detect_docker_image_os = groot_rocker.cli:detect_image_os'
        ],
        'groot_rocker.extensions': [
            'container_name = groot_rocker.extensions:ContainerName',
            'devices = groot_rocker.extensions:Devices',
            'env = groot_rocker.extensions:Environment',
            'home = groot_rocker.extensions:HomeDir',
            'network = groot_rocker.extensions:Network',
            'pulse = groot_rocker.extensions:PulseAudio',
        ]
    },
    'author': 'Daniel Stonier',
    'author_email': 'd.stonier@gmail.com',
    'keywords': ['Docker'],
    'classifiers': [
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License'
    ],
    'description': 'A tool to run docker containers with customized extras',
    'long_description': 'A tool to run docker containers with customized extra added like git gui support overlayed.',
    'license': 'Apache License 2.0',
    'python_requires': '>=3.0',

    'install_requires': install_requires,
    'extras_require':  extras_require,
    'url': 'https://github.com/stonier/groot_rocker'
}

setuptools.setup(**kwargs)
