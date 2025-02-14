# Copyright 2019 Open Source Robotics Foundation

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import grp
import os
import em
import pkgutil
from pathlib import Path
import re
from shlex import quote

from .core import get_docker_client


def name_to_argument(name):
    return '--%s' % name.replace('_', '-')

from .core import RockerExtension

class Devices(RockerExtension):
    @staticmethod
    def get_name():
        return 'devices'

    def __init__(self):
        self.name = Devices.get_name()

    def get_preamble(self, cliargs):
        return ''

    def get_docker_args(self, cliargs):
        args = ''
        devices = cliargs.get('devices', None)
        for device in devices:
            if not os.path.exists(device):
                print("ERROR device %s doesn't exist. Skipping" % device)
                continue
            args += ' --device %s ' % device
        return args

    @staticmethod
    def register_arguments(parser, defaults={}):
        parser.add_argument('--devices',
            default=defaults.get('devices', None),
            nargs='*',
            help="Mount devices into the container.")


class ContainerName(RockerExtension):
    @classmethod
    def get_name(cls):
        return re.sub(r'(?<!^)(?=[A-Z])', '_', cls.__name__).lower()  # CamelCase to underscores

    def get_preamble(self, cliargs):
        return ''

    def get_docker_args(self, cliargs):
        args = ''
        name = cliargs.get('container_name', None)
        if name:
            args += f' --name {name} '
        return args

    @staticmethod
    def register_arguments(parser, defaults={}):
        parser.add_argument(
            '--container-name',
            default=defaults.get(ContainerName.get_name(), None),
            metavar="NAME",
            help='human readable name for the container'
        )


class Network(RockerExtension):
    @staticmethod
    def get_name():
        return 'network'

    def __init__(self):
        self.name = Network.get_name()

    def get_preamble(self, cliargs):
        return ''

    def get_docker_args(self, cliargs):
        args = ''
        network = cliargs.get('network', None)
        args += ' --network %s ' % network
        return args

    @staticmethod
    def register_arguments(parser, defaults={}):
        client = get_docker_client()
        parser.add_argument('--network', choices=[n['Name'] for n in client.networks()],
            default=defaults.get('network', None),
            help="What network configuration to use.")


class HomeDir(RockerExtension):
    @staticmethod
    def get_name():
        return 'home'

    def __init__(self):
        self.name = HomeDir.get_name()

    def get_docker_args(self, cliargs):
        return ' -v %s:%s ' % (Path.home(), Path.home())

    @staticmethod
    def register_arguments(parser, defaults={}):
        parser.add_argument(name_to_argument(HomeDir.get_name()),
            action='store_true',
            default=defaults.get(HomeDir.get_name(), None),
            help="mount the users home directory")


class Environment(RockerExtension):
    @staticmethod
    def get_name():
        return 'env'

    def __init__(self):
        self.name = Environment.get_name()

    def get_snippet(self, cli_args):
        return ''

    def get_docker_args(self, cli_args):
        args = ['']

        if cli_args.get('env'):
            envs = [ x for sublist in cli_args['env'] for x in sublist]
            for env in envs:
                args.append('-e {0}'.format(quote(env)))

        if cli_args.get('env_file'):
            env_files = [ x for sublist in cli_args['env_file'] for x in sublist]
            for env_file in env_files:
                args.append('--env-file {0}'.format(quote(env_file)))

        return ' '.join(args)

    @staticmethod
    def register_arguments(parser, defaults={}):
        parser.add_argument('--env', '-e',
            metavar='NAME[=VALUE]',
            type=str,
            nargs='+',
            action='append',
            default=defaults.get(Environment.get_name(), []),
            help='set environment variables')
        parser.add_argument('--env-file',
            type=str,
            nargs=1,
            action='append',
            help='set environment variable via env-file')

    @classmethod
    def check_args_for_activation(cls, cli_args):
        """ Returns true if the arguments indicate that this extension should be activated otherwise false."""
        return True if cli_args.get('env') or cli_args.get('env_file') else False
