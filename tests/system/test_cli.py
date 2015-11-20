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
import oscli
from oscli import services, compat


class cliTest(unittest.TestCase):

    # Actions

    def setUp(self):
        self.openfiles = []
        self.data_dir = os.path.join(
                os.path.dirname(__file__), '..', '..', 'examples')
        self.dp_valid = os.path.join(self.data_dir, 'dp-valid')
        self.dp_invalid = os.path.join(self.data_dir, 'dp-invalid')
        self.data_valid = os.path.join(self.data_dir, 'data_valid.csv')
        self.data_invalid = os.path.join(self.data_dir, 'data_invalid.csv')

    # Helpers

    def check(self, *args):
        command =  ' '.join(['python -m oscli.cli'] + list(args))
        return subprocess.check_output(command, shell=True)

    def tearDown(self):
        if self.openfiles:
            for f in self.openfiles:
                f.close()

    def test_config_locate(self):
        expected = services.config.locate()
        actual = self.check('config locate')
        actual = actual.decode('utf-8').rstrip('\n')
        self.assertEqual(actual, expected)

    def test_config_read(self):
        expected = services.config.read()
        actual = self.check('config read')
        actual = json.loads(actual.decode('utf-8').rstrip('\n'))
        self.assertEqual(actual, expected)

    def test_validate_model_valid(self):
        actual = self.check('validate model', self.dp_valid)
        self.assertTrue(actual)

    def test_validate_model_invalid(self):
        self.assertRaises(
                subprocess.CalledProcessError,
                self.check, 'validate model', self.dp_invalid)

    def test_validate_data_valid(self):
        actual = self.check('validate data', self.dp_valid)
        self.assertTrue(actual)

    def test_validate_data_invalid(self):
        self.assertRaises(
                subprocess.CalledProcessError,
                self.check, 'validate data', self.dp_invalid)

    # def test_upload(self):

    #     c = ['python', '-m' 'oscli.cli',  'upload', self.dp_valid]
    #     result = subprocess.check_output(c)

    #     self.assertTrue(result)
