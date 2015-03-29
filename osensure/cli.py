# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import io
import json
import click
from . import lib


@click.command()
@click.argument('datapackage')
def main(datapackage):

    MSG_SUCCESS = ('Congratulations, the data looks good! You can now move on\n'
                   'to uploading your new data package to Open Spending!')
    MSG_CONTINUE = ('While checking the data, we found some found some issues\n'
                    'that need addressing. Shall we take a look?')
    MSG_CONTEXT = ('Note that not all errors are necessarily because of\n'
                   'invalid data. It could be that the schema needs adjusting\n'
                   'in order to represent the data more accurately.')
    MSG_GUIDE = ('Would you like to see our short guide on common schema\n'
                 'errors and solutions? (Launches a web page in your browser)')
    MSG_EDIT = ('Would you like to edit the schema for this data now? \n'
                '(Opens the file in your editor)')
    MSG_END_CONTINUE = ('That is all for now. Once you have made changes to\n'
                        'your data and/or schema, try running the ensure process again.')
    GUIDE_URL = 'https://github.com/openspending/etlcli-mvp/blob/master/osensure/guide.md'
    DESCRIPTOR = 'datapackage.json'

    ensure = lib.Ensure(datapackage)
    success = ensure.run()

    if success:
        click.echo(click.style(MSG_SUCCESS, fg='green'))

    else:
        if click.confirm(click.style(MSG_CONTINUE, fg='red')):
            click.clear()
            click.echo(click.style(lib.display_report(ensure.reports), fg='blue'))
            click.echo(click.style(MSG_CONTEXT, fg='green'))

        if click.confirm(click.style(MSG_GUIDE, fg='red')):
            click.launch(GUIDE_URL)

        if click.confirm(click.style(MSG_EDIT, fg='red')):
            click.edit(filename=os.path.join(datapackage, DESCRIPTOR))

        click.echo(click.style(MSG_END_CONTINUE, fg='green'))

if __name__ == '__main__':
    main()
