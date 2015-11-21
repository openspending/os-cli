# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import io
import json
import unittest
import subprocess
from click.testing import CliRunner
import oscli
from oscli import services


class cliTest(unittest.TestCase):

    # Actions

    def setUp(self):
        self.openfiles = []
        self.data_dir = os.path.join(
                os.path.dirname(__file__), '..', '..', 'examples')
        self.dp_valid = os.path.join(self.data_dir, 'dp-valid')
        self.dp_invalid = os.path.join(self.data_dir, 'dp-invalid')

    # Helpers

    def invoke(self, *args):
        runner = CliRunner()
        return runner.invoke(oscli.cli, args)

    def tearDown(self):
        if self.openfiles:
            for f in self.openfiles:
                f.close()

    def test_config_locate(self):
        result = self.invoke('config', 'locate')
        actual = result.output.rstrip('\n')
        expected = services.config.locate()
        self.assertEqual(actual, expected)

    def test_config_read(self):
        result = self.invoke('config', 'read')
        actual = json.loads(result.output.rstrip('\n'))
        expected = services.config.read()
        self.assertEqual(actual, expected)

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

    # def test_upload(self):

    #     c = ['python', '-m' 'oscli.cli',  'upload', self.dp_valid]
    #     result = subprocess.invoke_output(c)

    #     self.assertTrue(result)
