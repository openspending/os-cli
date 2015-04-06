# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import uuid
from . import base


class AuthService(base.OpenSpendingService):

    """Interact with an Open Spending Auth service."""

    DOMAIN = 'https://auth.openspending.org'

    def login(self):
        """Login and return a token."""
        return uuid.uuid4().hex

    def logout(self):
        """Logout and return success."""
        return True
