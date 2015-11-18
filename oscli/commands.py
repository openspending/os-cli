# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import json
import click
from oscli import upload as _upload
from . import compat, config, validate, utilities


@click.group()
def cli():
    """Open Spending CLI.
    """


@cli.command(name='config')
@click.argument('action', default='read',
    type=click.Choice(['locate', 'ensure', 'read', 'write']))
@click.argument('data', default='{}')
def command_config(action, data):
    """Interact with config in .openspendingrc

    Args:
    * action: one of 'read', 'locate' or 'ensure'
        * 'locate' will return the location of the currently active config
        * 'ensure' will check a config exists, and write one in $HOME if not
        * 'read' will return the currently active config
        * 'write' will add additional JSON data to config and return updated config

    """

    # Locate
    if action == 'locate':
        click.echo(config.Config.locate())

    # Ensure
    if action == 'ensure':
        click.echo(json.dumps(config.Config.ensure(), indent=4, ensure_ascii=False))

    # Read
    if action == 'read':
        click.echo(json.dumps(config.Config.read(), indent=4, ensure_ascii=False))

    # Write
    if action == 'write':
        try:
            data = json.loads(data)
            click.echo(json.dumps(config.Config.write(**data), indent=4, ensure_ascii=False))
        except Exception:
            raise ValueError('Data is a not valid config in JSON format.')


@cli.command(name='validate')
@click.argument('subcommand', type=click.Choice(['model', 'data']))
@click.argument('datapackage')
@click.option('--interactive', is_flag=True)
def command_validate(subcommand, datapackage, interactive):
    """Validate an Open Spending Data Package descriptor/data.

    Args:
    * subcommand: one of 'package' or 'data'
        * 'package' will validate a descriptor
        * 'data' will validate a data

    """

    # Vaildate model
    if subcommand == 'model':

        MSG_SUCCESS = ('Congratulations, the data package looks good!')
        MSG_ERROR = ('While checking the data, we found some found some '
                     'issues: \n{0}\nRead more about required fields in '
                     'Open Spending Data Package here: {1}')
        url = 'https://github.com/openspending/oscli-poc#open-spending-data-package'
        service = validate.ModelValidator(datapackage)
        service.run()
        if service.success:
            click.echo(click.style(MSG_SUCCESS))
        else:
            click.echo(click.style(MSG_ERROR.format(service.error, url)))

    # Validate data
    if subcommand == 'data':

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
        service = validate.DataValidator(datapackage)
        success = service.run()

        if success:

            click.echo(click.style(MSG_SUCCESS, fg='green'))

        else:

            report = validate.DataValidator.display_report(service.reports)

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


@cli.command()
@click.argument('datapackage', default='.', type=click.Path(exists=True))
def upload(datapackage):
    """Upload an Open Spending Data Package to storage. Requires auth.
    """

    # don't proceed without a config
    if not config.Config.locate():
        _msg = ('Uploading requires a config file. See the configuration '
                'section of the README for more information: '
                'https://github.com/openspending/oscli-poc')
        click.echo(click.style(_msg, fg='red'))
        return

    # is data package
    _valid, _msg = utilities.is_datapackage(datapackage)
    if not _valid:
        click.echo(click.style(_msg, fg='red'))
        return

    if isinstance(datapackage, compat.bytes):
        datapackage = datapackage.decode('utf-8')

    # is open spending data package
    checker = _checkmodel.Checker(datapackage)
    checker.run()
    if not checker.success:
        _msg = ('While checking the data, we found some found some '
                'issues: \n{0}\nRead more about required fields '
                'in Open Spending Data Packages here: {1}')
        url = 'https://github.com/openspending/oscli-poc#open-spending-data-package'
        click.echo(click.style(_msg.format(checker.error, url), fg='red'))
        return

    try:
        service = _upload.Upload()
    except Exception as exception:
        click.echo(click.style(exception.msg, fg='red'))
        return

    click.echo(click.style('Your data is now being uploaded to Open Spending.\n',
                           fg='green'))
    service.run(datapackage)
    click.echo(click.style('Your data is now live on Open Spending!',
                           fg='green'))


@cli.command()
def version():
    """Display the version and exit.
    """

    msg = 'There is no version tracking yet.'
    click.echo(msg)


if __name__ == '__main__':
    cli()
