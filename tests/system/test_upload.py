# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import unittest
import tempfile
from click.testing import CliRunner
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch
import oscli
from oscli import actions
from oscli import services
from oscli.actions import upload


class cli_upload_Test(unittest.TestCase):

    # Actions

    def setUp(self):

        # Cleanup
        self.addCleanup(patch.stopall)

        # Data packages
        self.data_dir = os.path.join(
                os.path.dirname(__file__), '..', '..', 'examples')
        self.dp_valid = os.path.join(self.data_dir, 'dp-valid')
        self.dp_invalid = os.path.join(self.data_dir, 'dp-invalid')

        # Config path
        _, self.herepath = tempfile.mkstemp()
        patch.object(services.config, 'HEREPATH', self.herepath).start()

        # Path validate model
        self.ValidateModel = patch.object(actions, 'ValidateModel').start()

        # Patch http requests
        self.requests = patch.object(upload, 'requests').start()
        self.requests.post.return_value.json.return_value = {
            'filedata': {
                'datapackage.json': {
                    'name': 'datapackage.json',
                    'length': 100,
                    'md5': 'md5',
                    'upload_url': 'url',
                    'upload_query': {'key': 'value'},
                },
            },
        }
        self.FuturesSession = patch.object(upload, 'FuturesSession').start()

    def tearDown(self):
        try:
            os.remove(self.herepath)
        except Exception:
            pass

    # Helpers

    def invoke(self, *args):
        runner = CliRunner()
        return runner.invoke(oscli.cli, args)

    # Tests

    def test_upload(self):
        result = self.invoke('upload', self.dp_valid)
        self.assertEqual(result.exit_code, 0)

    def test_upload_without_config(self):
        os.remove(self.herepath)
        result = self.invoke('upload', self.dp_valid)
        self.assertEqual(result.exit_code, 1)

    def test_upload_not_datapackage(self):
        result = self.invoke('upload', self.data_dir)
        self.assertNotEqual(result.exit_code, 0)

    def test_upload_with_error(self):
        self.requests.post.return_value = None
        result = self.invoke('upload', self.dp_valid)
        self.assertNotEqual(result.exit_code, 0)
