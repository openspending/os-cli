# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from .. import _mock
from .. import utilities
from .. import exceptions




    # if config is None or not config.get('token'):
    #     click.echo(click.style(MSG_NO_TOKEN))
    #     return

    # backend = _storage.StorageService(config['token'], config['username'])
    # storage_token = backend.get_storage_token(datapackage)

    # # update config
    # tokens = {'storage_tokens': {pkg.name: storage_token}}
    # if config.get('storage_tokens'):
    #     config['storage_tokens'].update(tokens['storage_tokens'])
    # else:
    #     config.update(tokens)

    # url = backend.upload(config['token'], stroage_token, config['username'], datapackage)

    # click.echo(click.style(url, fg='green'))

class Upload(object):

    """Upload a datapackage to the flat file store."""

    def __init__(self, config=None):

        self.config = config or utilities.read_config()

        try:
            self.backend = _mock.StorageService(self.config['token'],
                                                self.config['username'])
        except exceptions.InvalidSessionError as e:
            raise e

    def run(self, datapackage_path):
        """Run the upload flow."""
        self.backend.upload(datapackage_path)
