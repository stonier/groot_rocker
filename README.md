# Groot Rocker

A tool, inspired by tfoote's [rocker](https://github.com/osrf/rocker) package (and this may one day get back to being a strict fork of that).

# Overview

Problem-to-solve: Execute a command, but do it in an environment of my choosing (not necessarily your native system environment).

This package provides a console script `groot-rocker` that lets you specify the command of your choice along with options that help configure a sandboxed docker environment for that command to execute in. 

The **secret sauce** - behind the scenes the script will convert the options you've provided to configure the environment into `Dockerfile` snippets that are stitched together to help build the docker environment requested. In short, **reusable dockerfile patterns**. 

Want to transfer your git configuration? The **git** extension will do that. Map your current user into the docker environment? The **user** extension will do that. Mix and match as you please.

NB: docker caching will expedite the process, so that repeated execution will be almost as fast as just executing the command.

# Extensions

Reusable dockerfile configuration is encoded via `RockerExtension` implementations. There are several simple examples in this repository, but more complex ones are housed (or migrating) to external repositories.

* [groot_rocker_extensions](https://github.com/stonier/groot_rocker_extensions/blob/devel/README.md)

# Usage - Examples

See the extension repositories for examples.

# Usage - Cleanup

This script will generate unnamed/named images for each unique execution of `groot_rocker`. This can leave quite a few dangling images, especially
if you are frequently running with non-persistent containers. You can batch prune these with:

```
$ docker image prune
```
