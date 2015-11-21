import os
import unittest
from importlib import import_module
module = import_module('oscli.helpers.is_datapackage')


class is_datapackage_Test(unittest.TestCase):

    # Actions

    def setUp(self):

        # Data packages
        self.data_dir = os.path.join(
                os.path.dirname(__file__), '..', '..', '..', 'examples')
        self.dp_valid = os.path.join(self.data_dir, 'dp-valid')
        self.dp_invalid = os.path.join(self.data_dir, 'dp-invalid')

    # Tests

    def test_not_dir(self):
        self.assertFalse(module.is_datapackage(__file__)[0])

    def test_valid(self):
        self.assertTrue(module.is_datapackage(self.dp_valid)[0])

    def test_invalid(self):
        self.assertTrue(module.is_datapackage(self.dp_invalid)[0])
