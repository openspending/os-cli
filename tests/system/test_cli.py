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


    def setUp(self):
        self.openfiles = []
        self.data_dir = os.path.join(
                os.path.dirname(__file__), '..', '..', 'examples')
        self.dp_valid = os.path.join(self.data_dir, 'dp-valid')
        self.dp_invalid = os.path.join(self.data_dir, 'dp-invalid')
        self.data_valid = os.path.join(self.data_dir, 'data_valid.csv')
        self.data_invalid = os.path.join(self.data_dir, 'data_invalid.csv')

    def tearDown(self):
        if self.openfiles:
            for f in self.openfiles:
                f.close()

    def test_config(self):

        c = ['python', 'debug.py', 'config']
        expected = services.config.read()
        actual = subprocess.check_output(c)
        actual = json.loads(actual.decode('utf-8').rstrip('\n'))

        self.assertEqual(actual, expected)

    # def test_upload(self):

    #     c = ['python', 'debug.py', 'upload', self.dp_valid]
    #     result = subprocess.check_output(c)

    #     self.assertTrue(result)

    def test_validate_model(self):

        c = ['python', 'debug.py', 'validate', 'model', self.dp_valid]
        result = subprocess.check_output(c)

        self.assertTrue(result)

    def test_validate_data(self):

        c = ['python', 'debug.py', 'validate', 'data', self.dp_valid]
        result = subprocess.check_output(c)

        self.assertTrue(result)
