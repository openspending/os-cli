# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import io
import json


def is_datapackage(_path):
    """Ensure that _path is a Data Package.
    """

    # Descriptor name
    descriptor_name = 'datapackage.json'

    # Check it's a dir
    if not os.path.isdir(_path):
        MSG = ('The path is not a directory, and therefore not a valid '
               'Data Package.')
        return False, MSG

    # Check it has descriptor file
    descriptor = os.path.join(_path, descriptor_name)
    if not os.path.exists(descriptor):
        MSG = ('The directory does not include a {0}, and so is not a valid '
               'Data Package.'.format(descriptor_name))
        return False, MSG

    # Then a valid datapackage
    MSG = ('The path is a valid Data Package')
    return True, MSG
