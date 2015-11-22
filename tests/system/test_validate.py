# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import unittest
from click.testing import CliRunner
import oscli


class cli_validate_Test(unittest.TestCase):

    # Actions

    def setUp(self):

        # Data packages
        self.data_dir = os.path.join(
                os.path.dirname(__file__), '..', '..', 'examples')
        self.dp_valid = os.path.join(self.data_dir, 'dp-valid')
        self.dp_invalid = os.path.join(self.data_dir, 'dp-invalid')

    # Helpers

    def invoke(self, *args):
        runner = CliRunner()
        return runner.invoke(oscli.cli, args)

    # Tests

    def test_validate_model_valid(self):
        result = self.invoke('validate', 'model', self.dp_valid)
        self.assertEqual(result.exit_code, 0)

    def test_validate_model_invalid(self):
        result = self.invoke('validate', 'model', self.dp_invalid)
        self.assertEqual(result.exit_code, 1)

    def test_validate_data_valid(self):
        result = self.invoke('validate', 'data', self.dp_valid)
        self.assertEqual(result.exit_code, 0)

    def test_validate_data_invalid(self):
        result = self.invoke('validate', 'data', self.dp_invalid)
        self.assertEqual(result.exit_code, 1)
