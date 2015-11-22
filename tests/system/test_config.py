# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import io
import json
import unittest
import tempfile
from click.testing import CliRunner
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch
import oscli
from oscli import services


class cli_config_Test(unittest.TestCase):

    # Actions

    def setUp(self):

        # Config pathes
        self.addCleanup(patch.stopall)
        _, self.herepath = tempfile.mkstemp()
        _, self.homepath = tempfile.mkstemp()
        patch.object(services.config, 'HEREPATH', self.herepath).start()
        patch.object(services.config, 'HOMEPATH', self.homepath).start()

    def tearDown(self):
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

    def test_config_write(self):
        result = self.invoke('config', 'write', '{"key": "value"}')
        actual = json.loads(result.output.rstrip('\n'))
        expected = services.config.read()
        self.assertEqual(actual['key'], 'value')
        self.assertEqual(actual, expected)
