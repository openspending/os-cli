# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import io
import json
import hashlib


def is_datapackage(_path):
    """Ensure that _path is a Data Package.
    """

    descriptor_name = 'datapackage.json'

    if not os.path.isdir(_path):
        MSG = ('The path is not a directory, and therefore not a valid '
               'Data Package.')
        return False, MSG

    descriptor = os.path.join(_path, descriptor_name)
    if not os.path.exists(descriptor):
        MSG = ('The directory does not include a {0}, and so is not a valid '
               'Data Package.'.format(descriptor_name))
        return False, MSG

    MSG = ('The path is a valid Data Package')
    return True, MSG

def get_file_md5(path):
    """Get md5 checksum of a file by path.
    """
    hash = hashlib.md5()
    with open(path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            hash.update(chunk)
    return hash.hexdigest()
