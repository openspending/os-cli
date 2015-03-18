# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import datapackage
import budgetdatapackage
import jtskit


def infer_mapping(schema):

    """Infer an Open Spending Data Package."""

    mapping = {}
    schema_model = jtskit.models.JSONTableSchema(schema)

    if schema_model.has_field('id'):
        mapping['id'] = 'id'

    if schema_model.has_field('amount'):
        mapping['amount'] = 'amount'
    else:
        number_fields = schema_model.get_fields_by_type('number')
        if number_fields:
            if len(number_fields) == 1:
                mapping['amount'] = number_fields.pop(0)

    if schema_model.has_field('payer'):
        mapping['payer'] = 'payer'

    if schema_model.has_field('payer_id'):
        mapping['payer_id'] = 'payer_id'

    if schema_model.has_field('payee'):
        mapping['payee'] = 'payee'

    if schema_model.has_field('payee_id'):
        mapping['payee_id'] = 'payee_id'

    return mapping


def get_mapping_from_string(mapping_string):

    """Get a mapping from a mapping string.

    format: my_id=your_id,my_other_id=your+other_id

    """

    mapping = {}
    _args = mapping_string.split(',')

    for _a in _args:
        k, v = _a.split('=')
        mapping[k] = v

    return mapping


def create(name, resources, mapping):

    """Create an Open Spending Data Package."""

    return OpenSpendingDataPackage(**{
        'name': name,
        'resources': resources,
        'openspending': {
            'mapping': mapping
        }
    })


class OpenSpendingResource(budgetdatapackage.BudgetResource):

    """Model for loading and managing Open Spending Data Package resources."""

    # temp override
    REQUIRED = (('url', 'path', 'data'),)


class OpenSpendingDataPackage(datapackage.DataPackage):

    """Model for loading and managing Open Spending Data Packages."""

    RESOURCE_CLASS = OpenSpendingResource

    @property
    def openspending(self):
        return self['openspending']

    @openspending.setter
    def openspending(self, value):
        if not value:
            raise ValueError("resources is a required field")

            raise TypeError(
                '{0} must be a list not {1}'.format(
                    self.RESOURCE_CLASS.__name__, type(value)))

        self['openspending'] = value
