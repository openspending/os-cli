# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from .. import _mock
from .. import utilities


class Auth(object):

    def __init__(self):
        self.backend = _mock.AuthService()

    def login(self):
        """Login the user."""

        token = self.backend.login()
        utilities.write_config(**{'token': token})

        return token

    def logout(self):
        """Logout the user."""

        success = self.backend.logout()
        if success:
            utilities.write_config(**{'token': ''})

        return ''
