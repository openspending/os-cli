# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import json
import datapackage
from datapackage import compat
from . import resource


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

                     # openspending specific
                     'owner': compat.str,
                     'openspending': dict}

    REQUIRED = ('name', 'owner', 'openspending')
    RESOURCE_CLASS = resource.OpenSpendingResource

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
    def openspending(self):
        return self['openspending']

    @openspending.setter
    def openspending(self, value):
        if not value:
            raise ValueError("openspending is a required field")

            raise TypeError(
                'openspending must be a dict, not {1}'.format(type(value)))

        self['openspending'] = value

    def as_dict(self):
        """Override base to deal with resources."""
        _resources = [{k: v for k, v in r.items() if
                       k not in r.SERIALIZE_EXCLUDES}
                      for r in self.resources]
        as_dict = super(OpenSpendingDataPackage, self).as_dict()
        as_dict['resources'] = _resources
        return as_dict

    def as_json(self):
        return json.dumps(self.as_dict(), ensure_ascii=False, indent=4)
