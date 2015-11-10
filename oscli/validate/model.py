# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import io
import json
from .. import package


class ModelValidator(object):
    """Check that a descriptor is a valid Open Spending Data Package.
    """

    def __init__(self, datapackage):
        self.datapackage = datapackage
        self.descriptor_path = os.path.join(self.datapackage, 'datapackage.json')
        with io.open(self.descriptor_path, mode='r+t', encoding='utf-8') as f:
            self.descriptor = json.loads(f.read())
        self.success = None
        self.error = None

    def run(self):
        try:
            pakcage.OpenSpendingDataPackage(**self.descriptor)
            self.success = True
        except Exception as e:
            self.error = e
            self.success = False

        return self.success
