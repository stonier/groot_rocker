#
# License: BSD
#   https://raw.githubusercontent.com/stonier/groot_rocker/devel/LICENSE
#
##############################################################################
# Documentation
##############################################################################

"""
The command line client.
"""

##############################################################################
# Imports
##############################################################################

import argparse
import typing
import yaml

from . import console
from . import core
from . import os_detector
from . import version

##############################################################################
# Main
##############################################################################


def set_default(option: str, yaml_defaults: str) -> typing.Any:
    return yaml_defaults[option] if option in yaml_defaults else None

##############################################################################
# Main
##############################################################################


def load_arguments(
    command_line_arguments: typing.Optional[typing.List[str]]=None
) -> typing.Dict[str, typing.Any]:
    config_parser = argparse.ArgumentParser(add_help=False)
    config_parser.add_argument(
        '-c', '--config', type=str, metavar="YAML", default=None, help="pre-load options from a yaml file"
    )
    config_args, remaining_argv = config_parser.parse_known_args(command_line_arguments)

    yaml_defaults = {}
    if config_args.config is not None:
        with open(config_args.config, 'r') as stream:
            yaml_defaults = yaml.load(stream, yaml.loader.FullLoader)

    parser = argparse.ArgumentParser(
        parents=[config_parser],
        description='A tool for running docker with extra options',
        # formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        '-v', '--version', action='version', version='%(prog)s ' + version.__version__
    )

    build_options = parser.add_argument_group(title="Build Options")
    build_options.add_argument(
        '--nocache', action='store_true',
        default=set_default("nocache", yaml_defaults),
        help="do not use cache when building"
    )
    build_options.add_argument(
        '--pull', action='store_true',
        default=set_default("pull", yaml_defaults),
        help="always attempt to pull newer versions"
    )
    build_options.add_argument(
        '--image-name', type=str, metavar="NAME",
        default=set_default("image_name", yaml_defaults),
        help="image names in the form repo:tag"
    )

    run_options = parser.add_argument_group(title="Run Options")
    run_options.add_argument(
        '--persistent', action='store_true',
        default=set_default("persistent", yaml_defaults), help="persist the container post-execution"
    )

    parser.add_argument(
        'image', nargs='?',
        default=set_default("image", yaml_defaults),
        help="base image to build from (required)"
    )
    default_command = yaml_defaults["command"] if "command" in yaml_defaults else []
    if isinstance(default_command, str):  # user convenience
        default_command = default_command.split(' ')
    parser.add_argument('command', nargs='*', default=default_command, help="command to run upon entering the container")

    extensions = parser.add_argument_group(title="Extensions")

    try:
        extension_manager = core.RockerExtensionManager()
        extension_manager.extend_cli_parser(extensions, yaml_defaults)
    except core.DependencyMissing as ex:
        # Catch errors if docker is missing or inaccessible.
        parser.error("DependencyMissing encountered: %s" % ex)

    args = vars(parser.parse_args(remaining_argv))  # work with a dict object from here, not argparse.Namespace
    args["command"] = ' '.join(args["command"])  # Convert command into string

    return args


def main():
    build_and_run(load_arguments())


def build_and_run(options: typing.Dict[str, typing.Any]):
    extension_manager = core.RockerExtensionManager()
    active_extensions = extension_manager.get_active_extensions(options)
    console.banner("Command Line")
    print(console.green + "Options" + console.reset)
    for k, v in options.items():
        print(" - " + console.cyan + str(k) + console.reset + ": " + console.yellow + str(v) + console.reset)
    print(console.green + "\nActive Extensions" + console.reset)
    for e in active_extensions:
        print(" - " + console.cyan + e.get_name() + console.reset)
    base_image = options["image"]
    dig = core.DockerImageGenerator(active_extensions, options, base_image)
    exit_code = dig.build(**options)
    if exit_code != 0:
        console.error("Build failed exiting")
        return exit_code
    return dig.run(**options)


def detect_image_os():
    parser = argparse.ArgumentParser(description='Detect the os in an image')
    parser.add_argument('image')
    parser.add_argument(
        '--verbose', action='store_true', help='Display verbose output of the process'
    )

    args = parser.parse_args()

    results = os_detector.detect_os(args.image, print if args.verbose else None)
    print(results)
    if results:
        return 0
    else:
        return 1
