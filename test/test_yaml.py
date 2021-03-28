#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# License: BSD
#   https://raw.githubusercontent.com/stonier/groot_rocker/devel/LICENSE
#

##############################################################################
# Imports
##############################################################################

import os
import unittest

import groot_rocker

from . import utilities

##############################################################################
# Tests
##############################################################################


class ExtensionTestCase(unittest.TestCase):

    def test_defaults_from_yaml(self):
        path = os.path.dirname(os.path.realpath(__file__))
        config_yaml = os.path.join(path, 'config.yaml')
        options = groot_rocker.cli.load_arguments(
            command_line_arguments=['-c', config_yaml]
        )
        expected_options = {
            "image": "ubuntu:18.04",
            "container_name": "foo",
            "image_name": "groot:foo",
            "command": "/bin/bash --login -i"
        }
        print("\n")
        for k, v in expected_options.items():
            utilities.assert_details(text=k, expected=v, result=options[k])
            self.assertEqual(options[k], v)
