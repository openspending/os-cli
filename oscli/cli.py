# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import json
import click
from . import actions, helpers, services, compat


@click.group()
def cli():
    """Open Spending CLI.
    """


choices = ['locate', 'ensure', 'read', 'write']
@cli.command()
@click.argument('action', default='read', type=click.Choice(choices))
@click.argument('data', default='{}')
def config(action, data):
    """Interact with config in .openspendingrc,

    Args:
        action (str): one of 'locate', 'ensure', read', 'write'
            - 'locate' will return the location of the currently active config
            - 'ensure' will check a config exists and write one in $HOME if not
            - 'read' will return the currently active config
            - 'write' will add additional JSON data to config and return config
    """

    # Locate
    if action == 'locate':
        click.echo(services.config.locate())

    # Ensure
    if action == 'ensure':
        click.echo(json.dumps(
            services.config.ensure(), indent=4, ensure_ascii=False))

    # Read
    if action == 'read':
        click.echo(json.dumps(
            services.config.read(), indent=4, ensure_ascii=False))

    # Write
    if action == 'write':
        try:
            data = json.loads(data)
            click.echo(json.dumps(
                services.config.write(**data), indent=4, ensure_ascii=False))
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

        MSG_SUCCESS = ('Congratulations, the data package looks good!')
        MSG_ERROR = ('While checking the data, we found some found some '
                     'issues: \n{0}\nRead more about required fields in '
                     'Open Spending Data Package here: {1}')
        url = 'https://github.com/openspending/oscli-poc#open-spending-data-package'
        action = actions.ValidateModel(datapackage)
        action.run()
        if action.success:
            click.echo(click.style(MSG_SUCCESS))
        else:
            click.echo(click.style(MSG_ERROR.format(action.error, url)))

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
        action = actions.ValidateData(datapackage)
        success = action.run()

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
    """Upload an Open Spending Data Package to storage.

    Requires valid API key.

    Args:
        datapackage (str): path to datapackage
    """

    # Don't proceed without a config
    if not services.config.locate():
        msg = ('Uploading requires a config file. See the configuration '
                'section of the README for more information: '
                'https://github.com/openspending/oscli-poc')
        click.echo(click.style(msg, fg='red'))
        return

    # Decode datapackage from utf-8
    if isinstance(datapackage, compat.bytes):
        datapackage = datapackage.decode('utf-8')

    #  Don't proceed not valid datapackage
    valid, msg = helpers.is_datapackage(datapackage)
    if not valid:
        click.echo(click.style(msg, fg='red'))
        return

    # Don't proceed not open spending data package
    checker = actions.ValidateModel(datapackage)
    checker.run()
    if not checker.success:
        msg = ('While checking the data, we found some found some '
                'issues: \n{0}\nRead more about required fields '
                'in Open Spending Data Packages here: {1}')
        url = 'https://github.com/openspending/oscli-poc#open-spending-data-package'
        click.echo(click.style(msg.format(checker.error, url), fg='red'))
        return

    # Notify about uploading start
    msg = 'Your data is now being uploaded to Open Spending.'
    click.echo(click.style(msg, fg='green'))

    # Upload
    try:
        action = actions.Upload(datapackage)
        action.run()
    except Exception as exception:
        raise
        click.echo(click.style(repr(exception), fg='red'))
        return

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


if __name__ == '__main__':
    cli()
