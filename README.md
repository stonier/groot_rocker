# Groot Rocker

A tool, inspired by tfoote's [rocker](https://github.com/osrf/rocker) package (and this may one day get back to being a strict fork of that).

# Overview

* Customise an environment via command line arguments which translate into a Dockerfile
* Create that environment by building a docker image
* Execute a command in that environment via docker run

Docker caching will expedite that process, so that repeated execution will be almost as fast as the last step in the process.

# Usage

Setup a basic sandbox in the ubuntu distro of your choice (persistant ensures a container remains):

```
$ groot-rocker --user --name=myenvironment --work-directory=~ --persistant --named-prompt ubuntu:18.04 "/bin/bash --login -i
```

# CleanUp

This script will generate an unnamed image for each unique execution of `groot_rocker`. This can leave quite a few dangling images. Feel free to prune
these at any point in time with:

```
$ docker image prune
```
