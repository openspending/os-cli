# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import io
import json
import click
import goodtables
import jtskit
from . import osdatapackage
from . import utilities


@click.command()
@click.argument('data')
@click.argument('name')
@click.option('--datapackages')
@click.option('--mapping')
@click.option('--metadata')
@click.option('--archive')
def main(data, name, datapackages, mapping, metadata, archive):

    """Make an Open Spending Data Package from a CSV data source.

    Args:
        * `data`: path to data source
        * `name`: name of this data package
        * `datapackages`: path to directory for storing this data package
        * `mapping`: a mapping pattern of fields in source > fields in OSDP
        * `metadata`: a mapping pattern of meta data for this data source
        * `archive`: Path to archival material for this data package

    """

    if not datapackages:
        _home, _os, _models = os.path.expanduser('~'), 'openspending', 'datapackages'
        datapackages = os.path.join(_home, _os, _models)

    if not os.path.exists(datapackages):
        os.makedirs(datapackages)

    datapackage_path = os.path.join(datapackages, name)
    datatable = goodtables.datatable.DataTable(data)
    schema = jtskit.infer(datatable.headers, datatable.get_sample(20000))

    if mapping:
        mapping = osdatapackage.get_mapping_from_string(mapping)
    else:
        mapping = mapping or osdatapackage.infer_mapping(schema)

    metadata = osdatapackage.get_metadata(metadata, data)

    if not all([mapping.get('id'), mapping.get('amount')]):
        click.echo('Open Spending Data Packages require `id` and `amount` fields.')
        return

    if not all([metadata.get('currency'), metadata.get('granularity')]):
        click.echo('Open Spending Data Package Resources require `currency` and `granularity` fields.')
        return

    resource = {
        'path': data,
        'schema': schema,
    }
    resource.update(metadata)
    resources = [resource]
    descriptor = osdatapackage.create(name, resources, mapping)
    data_paths = [data]
    archive_paths = []

    utilities.persist_datapackage(descriptor, datapackage_path, data_paths,
                                  archive_paths)

    click.echo('Data has been modeled, and is now available at '
               '{0}'.format(datapackage_path))

if __name__ == '__main__':
    main()
