# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import io
import json


def map_from_string(mapping_string, separate=',', assign='='):

    """Extract a mapping object from a string.

    Args:
        * `mapping_string`: a string with expected mapping format
        * `separate`: separator for properties
        * `assign`: separator for keys, values

    Example:
        * key1=value1,key2=value2

    """

    return dict([arg.split(assign) for arg in mapping_string.split(separate)])


def is_datapackage(_path):
    """Ensure that _path is a Data Package."""

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
