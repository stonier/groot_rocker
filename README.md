# Groot Rocker

A tool, inspired by tfoote's [rocker](https://github.com/osrf/rocker) package (and this may one day get back to being a strict fork of that).

# Overview

Problem-to-solve: Execute a command, but do it in an environment of my choosing (not necessarily your native system environment).

This package provides a console script `groot-rocker` that lets you specify the command of your choice along with options that help configure a sandboxed docker environment for that command to execute in. 

The **secret sauce** - behind the scenes the script will convert the options you've provided to configure the environment into `Dockerfile` snippets that are stitched together to help build the docker environment requested. In short, **reusable dockerfile patterns**. 

Want to transfer your git configuration? The **git** extension will do that. Map your current user into the docker environment? The **user** extension will do that. Mix and match as you please.

NB: docker caching will expedite the process, so that repeated execution will be almost as fast as just executing the command.

# Extensions

Reusable dockerfile configuration is encoded via `RockerExtension` implementations.

# Usage - Examples

**Basic Development Sandbox**

```
$ groot-rocker --user --name=mydevenv --persistant --named-prompt ubuntu:18.04 "/bin/bash --login -i"
```

# Usage - Cleanup

This script will generate an unnamed image for each unique execution of `groot_rocker`. This can leave quite a few dangling images. Feel free to prune
these at any point in time with:

```
$ docker image prune
```
