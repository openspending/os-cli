# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from .. import _mock
from .. import utilities
from .. import mixins


class Auth(mixins.WithConfig):

    CONFIG_REQUIRES = ('api_key',)

    def __init__(self, config=None):
        super(Auth, self).__init__(config=config)
        self.backend = _mock.AuthService()

    def get_token(self):
        """Get a token."""
        token = self.backend.get_token(self.config['api_key'])
        utilities.write_config(**{'token': token})
        return token
