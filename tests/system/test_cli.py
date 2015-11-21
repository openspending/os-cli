# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import io
import json
import shutil
import unittest
import tempfile
import subprocess
from click.testing import CliRunner
try:
    from unittest.mock import Mock, patch
except ImportError:
    from mock import Mock, patch
import oscli
from oscli import services


class cliTest(unittest.TestCase):

    # Actions

    def setUp(self):

        # Data packages
        self.openfiles = []
        self.data_dir = os.path.join(
                os.path.dirname(__file__), '..', '..', 'examples')
        self.dp_valid = os.path.join(self.data_dir, 'dp-valid')
        self.dp_invalid = os.path.join(self.data_dir, 'dp-invalid')

        # Config pathes
        self.addCleanup(patch.stopall)
        _, self.herepath = tempfile.mkstemp()
        _, self.homepath = tempfile.mkstemp()
        patch.object(services.config, 'HEREPATH', self.herepath).start()
        patch.object(services.config, 'HOMEPATH', self.homepath).start()

    def tearDown(self):
        if self.openfiles:
            for file in self.openfiles:
                file.close()
        try:
            os.remove(self.herepath)
            os.remove(self.homepath)
        except Exception:
            pass

    # Helpers

    def invoke(self, *args):
        runner = CliRunner()
        return runner.invoke(oscli.cli, args)

    # Tests

    def test_config_locate_here(self):
        result = self.invoke('config', 'locate')
        actual = result.output.rstrip('\n')
        expected = self.herepath
        self.assertEqual(actual, expected)

    def test_config_locate_home(self):
        os.remove(self.herepath)
        result = self.invoke('config', 'locate')
        actual = result.output.rstrip('\n')
        expected = self.homepath
        self.assertEqual(actual, expected)

    def test_config_locate_null(self):
        os.remove(self.herepath)
        os.remove(self.homepath)
        result = self.invoke('config', 'locate')
        actual = result.output.rstrip('\n')
        expected = 'null'
        self.assertEqual(actual, expected)

    def test_config_ensure(self):
        os.remove(self.herepath)
        os.remove(self.homepath)
        result = self.invoke('config', 'ensure')
        actual = result.output.rstrip('\n')
        expected = self.homepath
        self.assertEqual(actual, expected)

    def test_config_read(self):
        result = self.invoke('config', 'read')
        actual = json.loads(result.output.rstrip('\n'))
        expected = services.config.read()
        self.assertEqual(actual, expected)

    def test_config_read_not_valid(self):
        with io.open(self.herepath, 'w', encoding='utf-8') as file:
            file.write('bad json')
        result = self.invoke('config', 'read')
        self.assertNotEqual(result.exit_code, 0)

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
