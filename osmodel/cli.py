# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import io
import click
import goodtables
import jtskit
from . import osdatapackage


@click.command()
@click.argument('data')
@click.argument('name')
@click.option('--datapackage')
@click.option('--mapping')
def main(data, datapackage, mapping):

    """Make an Open Spending Data Package from a CSV data source."""

    if not datapackage:
        _home, _os, _models = os.path.expanduser('~'), 'openspending', 'models'
        datapackage = os.path.join(_home, _os, _models)

    if not mapping:
        # guess the mapping?
        pass

    data = goodtables.utilities.data_table.DataTable(data)
    schema = jtskit.infer(data.headers, data.get_sample(20000))
    package = osdatapackage.infer(data, name, schema)

if __name__ == '__main__':
    main()
