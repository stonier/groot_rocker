# Groot Rocker

A tool, inspired by tfoote's [rocker](https://github.com/osrf/rocker) package (and this may one day get back to being a strict fork of that).

## Overview

Problem-to-solve: Execute a command, but do it in an environment of my choosing (not necessarily your native system environment).

This package provides a console script `groot-rocker` that lets you specify the command of your choice along with options that help configure a sandboxed docker environment for that command to execute in. 

The **secret sauce** - behind the scenes the script will convert the options you've provided to configure the environment into `Dockerfile` snippets that are stitched together to help build the docker environment requested. In short, **reusable dockerfile patterns**. 

Want to transfer your git configuration? The **git** extension will do that. Map your current user into the docker environment? The **user** extension will do that. Mix and match as you please.

NB: docker caching will expedite the process, so that repeated execution will be almost as fast as just executing the command.

## Installation

Currently tested and used on Ubuntu 18.04 with Python v3.

**Docker & NVidia**

```
# Docker
$ sudo apt install docker.io

# Nvidia Docker 2 - https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html#docker
#   Not required, but fetch if you want to enable the nvidia extension in groot_rocker_extensions
$ HOST_DISTRIBUTION=$(. /etc/os-release; echo $ID$VERSION_ID)
$ curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
$ curl -s -L https://nvidia.github.io/nvidia-docker/${HOST_DISTRIBUTION}/nvidia-docker.list | \
$ sudo tee /etc/apt/sources.list.d/nvidia-docker.list
$ sudo apt-get update
$ sudo apt-get -q -y install nvidia-docker2 > /dev/null
$ sudo systemctl restart docker
# Test
$ docker run --rm --gpus all nvidia/cuda:11.0-base nvidia-smi
```
**Groot Rocker**

From PyPi: `pip3 -U install groot_rocker`

In a Virtual Environment:
```
$ git clone https://github.com/stonier/groot_rocker.git ./groot_rocker
$ cd groot_rocker
$ . ./venv.bash
$ groot-rocker --help
# Build a .deb
$ make deb
```

From PPA: *coming soon*

## Usage

### Command Line

```
# A named bionic image / container with login and perisistence.
$ groot-rocker --image-name devel:foo --container-name foo --persistent ubuntu:18.04 "/bin/bash --login -i"

root@0d06be52d77c:/# uname -a
Linux 0d06be52d77c 4.15.0-128-generic #131-Ubuntu SMP Wed Dec 9 06:57:35 UTC 2020 x86_64 x86_64 x86_64 GNU/Linux
root@0d06be52d77c:/# exit

$ docker image ls

REPOSITORY          TAG                             IMAGE ID            CREATED             SIZE
workspace           bar                             32bcf5c7bce0        12 minutes ago      637MB

$ docker container ls

CONTAINER ID   IMAGE      COMMAND                 NAMES
0d06be52d77c   devel:foo  "/bin/bash --login -i"  foo

# Since it's persistent, it can be re-entered.
docker container start -i foo
```

See the additional extension repositories for more complex examples.

### From Yaml

As you might imagine, with a sufficient number of extensions, this might start driving even the most
meticulous person a little crazy. With a yaml file, can configure your requests.

Example configurations:

```
# partial.yaml
persistent: true
image: ubuntu:18.04
command: "/bin/bash --login -i"

# config.yaml
image_name: devel:foo
container_name: foo
persistent: true
image: ubuntu:18.04
command: "/bin/bash --login -i"
```
Example execution:

```
$ groot-rocker -c partial.yaml --image-name devel:foo --container-name foo
$ groot-rocker -c config.yaml
# Option overrides
$ groot-rocker -c config.yaml --image-name devel:bar --container-name bar
```

## Extensions

Reusable dockerfile configuration is encoded via `RockerExtension` implementations. There are several simple examples in this repository, but more complex ones are housed (or migrating) to external repositories.

* [groot_rocker_extensions](https://github.com/stonier/groot_rocker_extensions/blob/devel/README.md)

