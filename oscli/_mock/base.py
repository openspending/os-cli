# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


class OpenSpendingService(object):

    """Base interface to an Open Spending service."""

    DOMAIN = 'https://openspending.org/'

    def gatekeeper(self, token):
        """Can this user interact with this service with this token?"""
        return self._accept_token(token)

    def _accept_token(self, token):
        """Is this token valid?"""
        return True
