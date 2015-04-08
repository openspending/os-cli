# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import io
import json
import shutil
import copy
import goodtables
import jtskit
from .. import osdatapackage


class Modeler(object):

    """Make an Open Spending Data Package from a data source."""

    def __init__(self, data, schema=None, destination=None,
                 mapping=None, metadata=None, archive=None):

        self.data_source = data
        # this needs to be adjusted relative to destination
        self.data_path = os.path.basename(self.data_source)
        self.schema_source = schema
        self.datatable = self.get_datatable()
        self.schema = schema or self.infer_schema()
        self.mapping = mapping or self.infer_mapping()
        self.metadata = metadata or self.metadata_defaults
        self.descriptor = self.create_descriptor()
        self.destination = self.get_destination(destination)
        self.persist_in_place = bool(destination)
        self.archive = archive

    @property
    def metadata_defaults(self):
        return {
            'currency': 'USD',
            'granularity': 'aggregated',
            'name': os.path.splitext(os.path.basename(self.data_source))[0]
        }

    def get_destination(self, passed_destination):
        if passed_destination is not None:
            return passed_destination
        else:
            return os.path.dirname(self.data_source)

    def create_descriptor(self):

        resource = {
            'name': '',
            'title': '',
            'description': '',
            'path': self.data_path,
            'schema': self.schema
        }
        resource.update(self.metadata)

        package = {
            'name': 'your-package-name',
            'owner': 'username',
            'title': 'Your Package Name',
            'description': 'A friendly description of your Data Package.',
            'resources': [resource],
            'openspending': {
                'mapping': self.mapping
            }
        }

        return osdatapackage.OpenSpendingDataPackage(**package)

    def get_datatable(self):
        return goodtables.datatable.DataTable(self.data_source)

    def infer_schema(self):
        return jtskit.infer(self.datatable.headers,
                            self.datatable.get_sample(20000))

    def infer_mapping(self):
        """Infer an Open Spending Data Package."""

        mapping = {}
        _schema = copy.deepcopy(self.schema)
        schema_model = jtskit.models.JSONTableSchema(_schema)

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

        if schema_model.has_field('payerId'):
            mapping['payerId'] = 'payerId'

        if schema_model.has_field('payee'):
            mapping['payee'] = 'payee'

        if schema_model.has_field('payer'):
            mapping['payeeId'] = 'payeeId'

        return mapping

    def run(self):

        descriptor_path = os.path.join(self.destination, 'datapackage.json')

        # data_dir = os.path.join(self.destination, 'data')
        # archive_dir = os.path.join(self.destination, 'archive')

        # if not os.path.exists(data_dir):
        #     os.makedirs(data_dir)

        # if not os.path.exists(archive_dir):
        #     os.makedirs(archive_dir)

        with io.open(descriptor_path, mode='w+t', encoding='utf-8') as f:
            f.write(json.dumps(self.descriptor, ensure_ascii=False, indent=4))

        # if self.archive:
        #     for filepath in os.listdir(self.archive):
        #         shutil.copy2(f, archive_dir)

        # if not self.persist_in_place:
        #     shutil.copy2(self.data_source, data_dir)

        return True
