# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import datapackage
import budgetdatapackage
from datapackage import compat


class OpenSpendingResource(budgetdatapackage.BudgetResource):

    """Model for loading and managing Open Spending Data Package resources."""

    EXTENDABLE = True
    SPECIFICATION = {'currency': compat.str,
                     # 'dateLastUpdated': compat.str,
                     # 'datePublished': compat.str,
                     'fiscalYear': compat.str,
                     'granularity': compat.str,
                     # 'standard': compat.str,
                     # 'status': compat.str,
                     # 'type': compat.str,
                     'location': compat.str,
                     'url': compat.str,
                     'path': compat.str,
                     'data': None,
                     'name': compat.str,
                     'format': compat.str,
                     'mediatype': compat.str,
                     'encoding': compat.str,
                     'bytes': int,
                     'hash': compat.str,
                     'schema': (dict, datapackage.schema.Schema),
                     'sources': list,
                     'licenses': list}

    REQUIRED = (('url', 'path', 'data'), 'currency', 'granularity')
