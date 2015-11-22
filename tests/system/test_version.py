# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import unittest
from click.testing import CliRunner
import oscli


class cli_version_Test(unittest.TestCase):

    # Helpers

    def invoke(self, *args):
        runner = CliRunner()
        return runner.invoke(oscli.cli, args)

    # Tests

    def test_version(self):
        result = self.invoke('version')
        self.assertEqual(result.exit_code, 0)
