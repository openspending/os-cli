# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import io
import json
import datapackage_validate
from .. import services


class ValidateModel(object):
    """Check that a descriptor is a valid Open Spending Data Package.

    Args:
        path (str): Path to the datapackage dir.
    """

    def __init__(self, datapackage):
        self.datapackage = datapackage
        self.descriptor_path = os.path.join(
                self.datapackage, 'datapackage.json')
        with io.open(self.descriptor_path, mode='r+t', encoding='utf-8') as f:
            self.descriptor = json.loads(f.read())
        self.config = services.config.read()
        self.success = None
        self.error = None

    def run(self):
        """Run validation.
        """
        valid, errors = datapackage_validate.validate(
            self.descriptor, self.config['schema'])
        self.success = valid
        self.error = errors
        return self.success
