# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import datapackage
import budgetdatapackage
from . import resource


    #     if not all([mapping.get('id'), mapping.get('amount')]):
    #         raise exceptions
    # if not all([metadata.get('currency'), metadata.get('granularity')]):
    #     click.echo('Open Spending Data Package Resources require `currency` and `granularity` fields.')
    #     return


class OpenSpendingDataPackage(datapackage.DataPackage):

    """Model for loading and managing Open Spending Data Packages."""

    REQUIRED = ('name', 'title', 'description',
                ('openspending', ('id', 'amount', 'payer', 'payerId',
                                  'payee', 'payeeId')))
    RESOURCE_CLASS = resource.OpenSpendingResource

    @property
    def openspending(self):
        return self['openspending']

    @openspending.setter
    def openspending(self, value):
        if not value:
            raise ValueError("openspending is a required field")

            raise TypeError(
                'openspending must be a dict, not {1}'.format(type(value)))

        self['openspending'] = value
