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
@click.option('--archive')
def main(data, name, datapackages, mapping, archive):

    """Make an Open Spending Data Package from a CSV data source.

    Args:
        * `data`: path to data source
        * `name`: name of this data package
        * `datapackages`: path to directory for storing this data package
        * `mapping`: a mapping pattern of fields in source > fields in OSDP
        * `archive`: Path to archival material for this data package

    """

    if not datapackages:
        _home, _os, _models = os.path.expanduser('~'), 'openspending', 'datapackages'
        datapackage_path = os.path.join(_home, _os, _models, name)
    else:
        datapackage_path = os.path.join(datapackages, name)

    data = goodtables.datatable.DataTable(data)
    schema = jtskit.infer(data.headers, data.get_sample(20000))
    mapping = mapping or osdatapackage.infer_mapping(schema)
    descriptor = osdatapackage.create(data, name, schema, mapping)
    resources = [data]
    schemas = [schema]

    utilities.persist_datapackage(json.dump(descriptor, ensure_ascii=False),
                                  datapackage_path, resources, schemas, archive)

    click.echo('Data has been modeled, and is now available at '
               '{0}'.format(datapackage_path))

if __name__ == '__main__':
    main()
