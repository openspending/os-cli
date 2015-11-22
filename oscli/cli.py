# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import json
import click
from . import actions, helpers, services, compat
click.disable_unicode_literals_warning = True


@click.group()
def cli():
    """Open Spending CLI.
    """


@cli.command()
@click.argument(
        'action', default='read',
        type=click.Choice(['locate', 'ensure', 'read', 'write']))
@click.argument('data', default='{}')
def config(action, data):
    """Interact with config in .openspendingrc,

    Args:
        action (str): one of 'locate', 'ensure', read', 'write'
            - 'locate' will return the location of the config file
            - 'ensure' will check a config exists and write one in $HOME if not
            - 'read' will return the currently active config
            - 'write' will add additional JSON data to config and return config
    """

    # Locate
    if action == 'locate':
        path = services.config.locate()
        if not path:
            path = 'null'
        click.echo(path)

    # Ensure
    if action == 'ensure':
        path = services.config.ensure()
        click.echo(path)

    # Read
    if action == 'read':
        config = services.config.read()
        click.echo(json.dumps(config, indent=4, ensure_ascii=False))

    # Write
    if action == 'write':
        try:
            data = json.loads(data)
            config = services.config.write(**data)
            click.echo(json.dumps(config, indent=4, ensure_ascii=False))
        except Exception:
            raise ValueError('Data is a not valid config in JSON format.')


@cli.command()
@click.argument('subcommand', type=click.Choice(['model', 'data']))
@click.argument('datapackage')
@click.option('--interactive', is_flag=True)
def validate(subcommand, datapackage, interactive):
    """Validate an Open Spending Data Package descriptor/data.

    Args:
        subcommand (str): one of 'model' or 'data'
            - 'model' will validate a model
            - 'data' will validate a data
        datapackage (str): path to datapackage
        interactive (bool): use interactive approach
    """

    # Vaildate model
    if subcommand == 'model':

        # Prepare
        msg_success = ('Congratulations, the data package looks good!')
        msg_error = ('While checking the data, we found some found some '
                     'issues: \n{0}\nRead more about required fields in '
                     'Open Spending Data Package here: {1}')
        url = ('https://github.com/dataprotocols/schemas/blob/master/'
               'fiscal-data-package.json')

        # Run action
        action = actions.ValidateModel(datapackage)
        action.run()
        if action.success:
            click.echo(click.style(msg_success))
        else:
            click.echo(click.style(msg_error.format(action.error, url)))
            exit(1)

    # Validate data
    if subcommand == 'data':

        # Prepare
        msg_success = (
                '\nCongratulations, the data looks good! You can now move on\n'
                'to uploading your new data package to Open Spending!')
        msg_context = (
                'IMPORTANT: Not all errors are necessarily because of\n'
                'invalid data. It could be that the schema needs adjusting\n'
                'in order to represent the data more accurately.')
        guide_url = ('https://github.com/openspending/os-datastore-cli/'
                     'blob/master/GUIDE.md')

        # Run action
        action = actions.ValidateData(datapackage)
        success = action.run()
        if success:
            click.echo(click.style(msg_success, fg='green'))
        else:
            report = actions.ValidateData.display_report(action.reports)
            click.echo(click.style(report, fg='blue'))
            click.echo(click.style(msg_context, fg='yellow'))
            click.echo('Read the guide for help:\n')
            click.echo(guide_url)
            exit(1)


@cli.command()
@click.argument('datapackage', default='.', type=click.Path(exists=True))
def upload(datapackage):
    """Upload an Open Spending Data Package to storage.

    Requires valid API key.

    Args:
        datapackage (str): path to datapackage
    """

    # Decode datapackage from utf-8
    if isinstance(datapackage, compat.bytes):
        datapackage = datapackage.decode('utf-8')

    # Don't proceed without a config
    if not services.config.locate():
        msg = ('Uploading requires a config file. See the configuration '
               'section of the README for more information: '
               'https://github.com/openspending/os-datastore-cli')
        click.echo(click.style(msg, fg='red'))
        exit(1)

    #  Don't proceed not valid datapackage
    valid, msg = helpers.is_datapackage(datapackage)
    if not valid:
        click.echo(click.style(msg, fg='red'))
        exit(1)

    # Don't proceed not open spending data package
    checker = actions.ValidateModel(datapackage)
    checker.run()
    if not checker.success:
        msg = ('While checking the data, we found some found some '
               'issues: \n{0}\nRead more about required fields '
               'in Open Spending Data Packages here: {1}')
        url = ('https://github.com/openspending/oscli-poc'
               '#open-spending-data-package')
        click.echo(click.style(msg.format(checker.error, url), fg='red'))
        exit(1)

    # Notify about uploading start
    msg = 'Your data is now being uploaded to Open Spending.'
    click.echo(click.style(msg, fg='green'))

    # Upload
    try:
        action = actions.Upload(datapackage)
        action.run()
    except Exception as exception:
        click.echo(click.style(repr(exception), fg='red'))
        exit(1)

    # Notify about uploading end
    msg = 'Your data is now live on Open Spending!'
    click.echo(click.style(msg, fg='green'))


@cli.command()
def version():
    """Display the version and exit.
    """

    # Notify no version for now
    msg = 'There is no version tracking yet.'
    click.echo(msg)


# Run `python -m oscli/cli`
if __name__ == '__main__':
    cli()
