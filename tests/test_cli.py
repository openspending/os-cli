# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import io
import json
import subprocess
from oscli import utilities
from oscli import compat
from tests import base


class TestCLI(base.BaseTestCase):

    def setUp(self):
        super(TestCLI, self).setUp()
        self.dp_valid = os.path.join(self.data_dir, 'dp-valid')
        self.dp_invalid = os.path.join(self.data_dir, 'dp-invalid')
        self.data_valid = os.path.join(self.data_dir, 'data_valid.csv')
        self.data_invalid = os.path.join(self.data_dir, 'data_invalid.csv')

    def tearDown(self):
        super(TestCLI, self).tearDown()

    def test_config(self):

        c = ['python', 'oscli/main.py', 'config']
        result = subprocess.check_output(c)
        config = utilities.read_config()
        result = json.loads(result.decode('utf-8').rstrip('\n'))

        self.assertEqual(result, config)

    def test_auth_login(self):

        c = ['python', 'oscli/main.py', 'auth', 'login']
        result = subprocess.check_output(c)
        config = utilities.read_config()
        result = result.decode('utf-8').rstrip('\n')

        self.assertEqual(result, config.get('token', ''))

    def test_auth_logout(self):

        c = ['python', 'oscli/main.py', 'auth', 'logout']
        result = subprocess.check_output(c)
        config = utilities.read_config()
        result = result.decode('utf-8').rstrip('\n')
        self.assertEqual(result, config.get('token', ''))

    # def test_upload(self):

    #     c = ['python', 'oscli/main.py', 'upload', self.dp_valid]
    #     result = subprocess.check_output(c)

    #     self.assertTrue(result)

    def test_makemodel_valid(self):

        c = ['python', 'oscli/main.py', 'makemodel', self.data_valid]
        result = subprocess.check_output(c)

        self.assertTrue(result)

    def test_makemodel_invalid(self):

        c = ['python', 'oscli/main.py', 'makemodel', self.data_invalid]
        result = subprocess.check_output(c)

        self.assertTrue(result)

    def test_checkmodel(self):

        c = ['python', 'oscli/main.py', 'checkmodel', self.dp_valid]
        result = subprocess.check_output(c)

        self.assertTrue(result)

    def test_checkdata(self):

        c = ['python', 'oscli/main.py', 'checkdata', self.dp_valid]
        result = subprocess.check_output(c)

        self.assertTrue(result)
