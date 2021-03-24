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

from . import console
from . import core
from . import os_detector
from . import version

##############################################################################
# Main
##############################################################################


def main():

    parser = argparse.ArgumentParser(
        description='A tool for running docker with extra options'
    )
    parser.add_argument(
        '-v', '--version', action='version', version='%(prog)s ' + version.__version__
    )

    image_options = parser.add_argument_group(title="Image Options", description="These options are transferred to 'docker image build'.")
    image_options.add_argument('--nocache', action='store_true', help="do not use cache when building")
    image_options.add_argument('--pull', action='store_true', help="always attempt to pull newer versions")
    image_options.add_argument('--tag', type=str, default=None, help="image identifiers in the form name:tag")

    run_options = parser.add_argument_group(title="Run Options", description="These options are transferred to 'docker run'.")
    run_options.add_argument('--persistent', action='store_true', help="persist the container post-execution")

    parser.add_argument('image')
    parser.add_argument('command', nargs='*', default='')

    extensions = parser.add_argument_group(title="Extensions")

    try:
        extension_manager = core.RockerExtensionManager()
        default_args = {}
        extension_manager.extend_cli_parser(extensions, default_args)
    except core.DependencyMissing as ex:
        # Catch errors if docker is missing or inaccessible.
        parser.error("DependencyMissing encountered: %s" % ex)

    args = parser.parse_args()
    args_dict = vars(args)

    active_extensions = extension_manager.get_active_extensions(args_dict)
    # Force user to end if present otherwise it will break other extensions
    active_extensions.sort(key=lambda e: e.get_name().startswith('user'))
    console.banner("Command Line")
    print(console.green + "Active Extensions" + console.reset)
    for e in active_extensions:
        print(" - " + console.cyan + e.get_name() + console.reset)

    base_image = args.image

    dig = core.DockerImageGenerator(active_extensions, args_dict, base_image)
    exit_code = dig.build(**vars(args))
    if exit_code != 0:
        console.error("Build failed exiting")
        return exit_code
    # Convert command into string
    args.command = ' '.join(args.command)
    return dig.run(**args_dict)


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
