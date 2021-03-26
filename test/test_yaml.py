#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# License: BSD
#   https://raw.githubusercontent.com/stonier/groot_rocker_extensions/devel/LICENSE
#

##############################################################################
# Imports
##############################################################################

import unittest

import groot_rocker

from . import utilities

##############################################################################
# Tests
##############################################################################


class ExtensionTestCase(unittest.TestCase):

    def test_defaults_from_yaml(self):
        options = groot_rocker.cli.load_arguments(
            command_line_arguments=['-c', 'config.yaml']
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
