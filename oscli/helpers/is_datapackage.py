# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import io
import json


def is_datapackage(path):
    """Ensure that path is a Data Package.
    """

    # Descriptor name
    descriptor_name = 'datapackage.json'

    # Check it's a directory
    if not os.path.isdir(path):
        msg = ('The path is not a directory, and therefore not a valid '
               'Data Package.')
        return False, msg

    # Check it has descriptor file
    descriptor = os.path.join(path, descriptor_name)
    if not os.path.exists(descriptor):
        msg = ('The directory does not include a {0}, and so is not a valid '
               'Data Package.'.format(descriptor_name))
        return False, msg

    # Then a valid datapackage
    msg = ('The path is a valid Data Package')
    return True, msg
