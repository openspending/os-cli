# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import io
import json
import click
from oscli import makemodel as _makemodel
from oscli import checkmodel as _checkmodel
from oscli import checkdata as _checkdata
from oscli import auth as _auth
from oscli import upload as _upload
from oscli import utilities


@click.group()
def cli():
    pass


@cli.command()
def version():

    """Display the version and exit."""

    msg = 'There is no version tracking yet.'
    click.echo(msg)


@cli.command()
def config():

    """Interact with .openspendingrc"""

    click.echo(json.dumps(utilities.ensure_config(), ensure_ascii=False))


@cli.command()
@click.argument('action', type=click.Choice(['login', 'logout']))
def auth(action):

    """Authenticate with the Open Spending auth service."""

    service = _auth.Auth()
    result = getattr(service, action)()
    click.echo(result)


@cli.command()
@click.argument('datapackage', default='.', type=click.Path(exists=True))
def upload(datapackage):

    """Upload an Open Spending Data Package to storage. Requires auth."""
    _valid, _msg = utilities.is_datapackage(datapackage)

    if not _valid:
        click.echo(click.style(_msg, fg='red'))
        return

    service = _upload.Upload()

    service.run(datapackage)
    click.echo(click.style('Done', fg='green'))


@cli.command()
@click.argument('data')
@click.option('--mapping')
@click.option('--metadata')
@click.option('--archive')
def makemodel(data, mapping, metadata, archive):

    """Model data as an Open Spending Data Package.

    Args:
        * `data`: path to data source
        * `datapackages`: path to directory for storing this data package
        * `mapping`: a mapping pattern of fields in source > fields in OSDP
        * `metadata`: a mapping pattern of meta data for this data source
        * `archive`: Path to archival material for this data package

    """

    # if not datapackages:
    #     _home, _os, _models = os.path.expanduser('~'), 'openspending', 'datapackages'
    #     datapackages = os.path.join(_home, _os, _models)

    # if not os.path.exists(datapackages):
    #     os.makedirs(datapackages)

    # datapackage_path = os.path.join(datapackages, name)

    if mapping:
        mapping = utilities.map_from_string(mapping)

    if metadata:
        metadata = utilities.map_from_string(metadata)

    service = _makemodel.Modeler(data, mapping=mapping, metadata=metadata,
                                 archive=archive)

    service.run()

    MSG = ('Well done. You have successfully modeled an Open Spending '
           'Data Package for your data. '
           'See it here: {0}'.format(service.destination))
    click.echo(MSG)


@cli.command()
@click.argument('datapackage')
def checkmodel(datapackage):

    """Check an Open Spending Data Package descriptor."""

    MSG_SUCCESS = ('Congratulations, the data package looks good!')
    MSG_ERROR = ('While checking the data, we found some found some '
                 'issues: {0}')

    service = _checkmodel.Checker(datapackage)
    service.run()
    if service.success:
        click.echo(click.style(MSG_SUCCESS))
    else:
        click.echo(click.style(MSG_ERROR.format(service.error)))


@cli.command()
@click.argument('datapackage')
@click.option('--interactive', is_flag=True)
def checkdata(datapackage, interactive):

    """Check data in an Open Spending Data Package descriptor."""

    MSG_SUCCESS = ('\nCongratulations, the data looks good! You can now move on\n'
                   'to uploading your new data package to Open Spending!')
    MSG_CONTINUE = ('While checking the data, we found some found some issues\n'
                    'that need addressing. Shall we take a look?')
    MSG_CONTEXT = ('IMPORTANT: Not all errors are necessarily because of\n'
                   'invalid data. It could be that the schema needs adjusting\n'
                   'in order to represent the data more accurately.')
    MSG_GUIDE = ('\nWould you like to see our short guide on common schema\n'
                 'errors and solutions? (Launches a web page in your browser)')
    MSG_EDIT = ('\nWould you like to edit the schema for this data now? \n'
                '(Opens the file in your editor)')
    MSG_END_CONTINUE = ('\nThat is all for now. Once you have made changes to\n'
                        'your data and/or schema, try running the ensure process again.')
    GUIDE_URL = 'https://github.com/openspending/oscli-poc/blob/master/oscli/checkdata/guide.md'
    DESCRIPTOR = 'datapackage.json'

    datapackage = os.path.abspath(datapackage)
    service = _checkdata.Checker(datapackage)
    success = service.run()

    if success:
        click.echo(click.style(MSG_SUCCESS, fg='green'))

    else:

        report = _checkdata.display_report(service.reports)
        if interactive:
            if click.confirm(click.style(MSG_CONTINUE, fg='red')):
                click.clear()
                click.echo(click.style(report, fg='blue'))
                click.echo(click.style(MSG_CONTEXT, fg='yellow'))

            if click.confirm(click.style(MSG_GUIDE, fg='yellow')):
                click.launch(GUIDE_URL)

            if click.confirm(click.style(MSG_EDIT, fg='yellow')):
                click.edit(filename=os.path.join(datapackage, DESCRIPTOR))

        else:
            click.echo(click.style(report, fg='blue'))
            click.echo(click.style(MSG_CONTEXT, fg='yellow'))
            click.echo('Read the guide for help:\n')
            click.echo(GUIDE_URL)

        click.echo(click.style(MSG_END_CONTINUE, fg='green'))


if __name__ == '__main__':
    cli()
