# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import io
import json
import boto
from . import base
from . import auth
from .. import exceptions
from .. import compat


class StorageService(base.OpenSpendingService):

    """Interact with an Open Spending Storage service."""

    DOMAIN = 'https://storage.openspending.org'
    AUTH_SERVICE = auth.AuthService
    BUCKET = os.environ.get('OPENSPENDING_STORAGE_BUCKET_NAME')
    AWS_ACCESS_KEY_ID = os.environ.get('OPENSPENDING_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('OPENSPENDING_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = BUCKET
    AWS_S3_CUSTOM_DOMAIN = DOMAIN
    AWS_S3_SECURE_URLS = True
    AWS_QUERYSTRING_AUTH = False
    ACCESS_KEY_EXPIRES_IN = 60 * 60 * 24 * 3  # 3 days to upload package

    def __init__(self):
        self.connection = boto.connect_s3(self.AWS_ACCESS_KEY_ID,
                                          self.AWS_SECRET_ACCESS_KEY)
        self.bucket = self.connection.get_bucket(self.BUCKET)
        self.auth = self.AUTH_SERVICE()

    def get_upload_access(self, api_key, token, descriptor, payload):
        """Get an access URL for each file in payload.

        Args:
            * payload (list of dicts): {'name': '', 'md5': ''}
        
        Returns:
            * list of payload with additional 'upload_url' key
        """
        verified = self.auth.verify(api_key, token, descriptor['owner'])
        if not verified:
            raise exceptions.InvalidCredentials
    
        for _file in payload:
            s3path = self.get_s3path(descriptor['owner'], descriptor['name'],
                                     _file['name'])
            s3key = self.get_s3key(s3path)
            s3headers = {'Content-MD5': _file['md5'],
                         'Content-Length': _file['length']}
            _file['upload_to'] = s3key.generate_url(self.ACCESS_KEY_EXPIRES_IN,
                                                    'PUT', headers=s3headers)

        return payload

    def get_s3key(self, s3path):
        """Return an S3 Key instance."""
        return self.bucket.new_key(s3path)

    def get_s3path(self, owner, pkgname, filename):
        """Return a path in this bucket for this file."""
        return '{0}/{1}'.format(pkgname, filename)
