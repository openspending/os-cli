# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import datapackage
import budgetdatapackage


class OpenSpendingResource(datapackage.Resource):

    """Model for loading and managing Open Spending Data Package resources."""

    # temp override
    REQUIRED = (('url', 'path', 'data'), 'currency', 'granularity')
    EXTENDABLE = True
