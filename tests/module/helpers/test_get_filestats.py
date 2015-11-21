import io
import os
import hashlib
import unittest
from base64 import b64encode
from importlib import import_module
module = import_module('oscli.helpers.get_filestats')


class get_filestats_Test(unittest.TestCase):

    # Tests

    def test(self):
        contents = io.open(__file__, 'rb').read()
        md5, length = module.get_filestats(__file__)
        self.assertEqual(md5, b64encode(hashlib.md5(contents).digest()).decode('utf-8'))
        self.assertEqual(length, str(os.path.getsize(__file__)))
