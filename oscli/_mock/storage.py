# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import io
import hashlib
import boto
from . import base
from .. import osdatapackage
from .. import exceptions


def get_checksum(filepath, blocksize=65536):

    """Make an MD5 hash from contents of a file."""

    hasher = hashlib.md5()
    with io.open(filepath, mode='r+t', encoding='utf-8') as stream:
        _buffer = stream.read(blocksize)
        while len(_buffer) > 0:
            hasher.update(_buffer)
            _buffer = stream.read(blocksize)

    return hasher.digest()


def get_filename(filepath):
    return os.path.basename(filepath)[1]


def upload_progress(bytes_sent, total_bytes):
    return bytes_sent, total_bytes


class StorageService(base.OpenSpendingService):

    """Interact with an Open Spending Storage service."""

    DOMAIN = 'https://storage.openspending.org'
    BUCKET = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = BUCKET
    AWS_S3_CUSTOM_DOMAIN = DOMAIN
    AWS_S3_SECURE_URLS = True
    AWS_QUERYSTRING_AUTH = False

    def __init__(self, token, username):

        if not self.gatekeeper(token):
            raise exceptions.InvalidSessionError

        self.token = token
        self.username = username
        self.connection = boto.connect_s3(self.AWS_ACCESS_KEY_ID,
                                          self.AWS_SECRET_ACCESS_KEY)
        self.bucket = self.connection.get_bucket(self.BUCKET)

    def get_storage_token(self, datapackage):
        storage_token = 'STORAGE_TOKEN'
        return storage_token

    def upload(self, storage_token, datapackage):
        """Upload a datapackage to an Open Spending data store."""
        # TODO: get descriptor out of datapackage
        pkg = osdatapackage.OpenSpendingDataPackage()
        workspace = self.bucket.list(prefix=self.username)
        for _file in self.get_payload(datapackage):
            _file['s3_key'].set_contents_from_filename(_file['local_path'],
                                                       md5=_file['md5'],
                                                       cb=upload_progress)

        return '{0}/{1}/{2}/'.format(self.DOMAIN, self.username, pkg.name)

    def get_payload(self, datapackage):
        """Return a generator of dicts."""
        return (self.get_file_payload(datapackage, filepath) for
                filepath in self._walker(datapackage))

    def get_s3key(self, s3path):
        """Return an S3 Key instance."""
        return self.bucket.new_key(s3path)

    def get_s3path(self, datapackage_name, filepath):
        """Return a path in this bucket for this file."""
        return '{0}/{1}'.format(datapackage_name, filepath)

    def get_file_payload(self, datapackage, filepath):
        """Return a file payload object."""
        _s3_path = self.get_s3path(datapackage.name, filepath)
        return {
            'local_path': filepath,
            'name': get_filename(filepath),
            'md5': get_checksum(filepath),
            's3_path': _s3_path,
            's3_key': self.get_s3key(_s3_path)
        }

    def _walker(self, datapackage):
        """Return all files in a datapackage."""
        return os.walk(datapackage)[2]
