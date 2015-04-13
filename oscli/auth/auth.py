# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from .. import _mock
from .. import utilities


class Auth(object):

    def __init__(self, config=None):
        self.config = config or utilities.read_config()
        self.backend = _mock.AuthService()

    def get_token(self):
        """Get a token."""
        token = self.backend.get_token(self.config['api_key'])
        utilities.write_config(**{'token': token})
        return token
