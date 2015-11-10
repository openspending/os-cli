# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import json
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


class OpenSpendingDataPackage(datapackage.DataPackage):

    """Model for loading and managing Open Spending Data Packages."""

    EXTENDABLE = True
    SPECIFICATION = {'name': compat.str,
                     'resources': list,
                     'license': compat.str,
                     'licenses': list,
                     'datapackage_version': compat.str,
                     'title': compat.str,
                     'description': compat.str,
                     'homepage': compat.str,
                     'version': compat.str,
                     'sources': list,
                     'keywords': list,
                     'image': compat.str,
                     'maintainers': list,
                     'contributors': list,
                     'publishers': list,
                     'base': compat.str,
                     'dataDependencies': dict,

                     # addition based on https://github.com/dataprotocols/dataprotocols/issues/87
                     'profiles': dict,
                     # openspending specific
                     'owner': compat.str,
                     'openspending': dict}

    REQUIRED = ('name', 'owner', 'openspending')
    RESOURCE_CLASS = OpenSpendingResource

    def ensure_required(self, kwargs):
        """Override base to provide additional Open Spending checks."""

        missing_fields = super(OpenSpendingDataPackage, self).ensure_required(kwargs)
        if not 'openspending' in missing_fields:
            extra = self.ensure_openspending_required(**kwargs.get('openspending', {}))
            missing_fields.extend(extra)

        return missing_fields

    def ensure_openspending_required(self, **kwargs):
        # NOTE: the openspending dict should look like:
        # {
        #     'openspending': {
        #         'mapping': {
        #             'id': 'SOMETHING',  # required, string
        #             'amount': 'SOMETHING',  # required, number
        #             'payee': 'SOMETHING',  # string
        #             'payeeId': 'SOMETHING',  # string
        #             'payer': 'SOMETHING',  # string
        #             'payerid': 'SOMETHING'  # string
        #         }
        #     }
        # }

        missing = []
        mapping = kwargs.get('mapping')

        if not mapping or not isinstance(mapping, dict):
            missing.append('mapping')
        elif not mapping.get('id'):
            missing.append('mapping > id')
        elif not mapping.get('amount'):
            missing.append('mapping > amount')

        return missing

    @property
    def profiles(self):
        return {
            'openspending': '*'
        }

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
