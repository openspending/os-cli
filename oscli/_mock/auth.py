# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from . import base


class AuthService(base.OpenSpendingService):

    """Interact with an Open Spending Auth service."""

    DOMAIN = 'https://auth.openspending.org'
    # MOCK: Keys and a list of their valid tokens
    API_KEYS = {
        '0c5f9c932f9c4196aacba5166380775d': {
            'username': 'user1',
            'token': '22bcb759f98a49339b335545d87dcbee',
            'permissions': ['user1', 'user2']
        },
        'a058790b30444991b2a6ad027c6dd619': {
            'username': 'user2',
            'token': '171d99a23c4e409caa5dee9500615a21',
            'permissions': ['user2']
        },
        'c57248b227d34abd8e4428f618ef6243': {
            'username': 'user3',
            'token': '1ead660dc21746aaab876f28d67b92ea',
            'permissions': ['user3']
        }
    }

    def verify(self, api_key, token, owner):
        """Verify credentials."""
        if (api_key in self.API_KEYS) and \
                (token == self.API_KEYS[api_key]['token']) and \
                (owner in self.API_KEYS[api_key]['permissions']):
            return True
        return False

    def get_token(self, api_key):
        """Return a token for the API Key."""

        match = api_key in self.API_KEYS

        if not match:
            return None

        return self.API_KEYS[api_key]['token']
