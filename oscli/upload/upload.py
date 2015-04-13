# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import io
import hashlib
import requests
from .. import osdatapackage
from .. import _mock
from .. import utilities
from .. import exceptions
from .. import compat


def get_checksum(filepath, blocksize=65536):
    """Return an MD5 hash of file contents of at filepath."""

    hasher = hashlib.md5()
    with io.open(filepath, mode='r+b') as stream:
        _buffer = stream.read(blocksize)
        while len(_buffer) > 0:
            hasher.update(_buffer)
            _buffer = stream.read(blocksize)

    return hasher.digest()


def get_contentlength(filepath):
    """Return an MD5 hash of file contents of at filepath."""

    with io.open(filepath, mode='r+t', encoding='utf-8') as stream:
        # TODO: temp while working out stuff: should make length while iterating
        length = len(stream.read())

    return compat.str(length)


def get_filestats(filepath):
    """Get stats on a file via iteration over its contents."""
    # TODO: Use this call to get_checksum and get_contentlength,
    # and build them both on iteration
    return


def get_filename(filepath):
    """Return the actual filename from the filepath."""
    return os.path.basename(filepath)


class Upload(object):

    """Upload a datapackage to the flat file store."""

    def __init__(self, config=None):
        self.config = config or utilities.read_config()
        try:
            self.backend = _mock.StorageService()
        except exceptions.InvalidSessionError as e:
            raise e

    def run(self, datapackage):
        """Run the upload flow."""

        pkg = osdatapackage.OpenSpendingDataPackage(datapackage)
        payload = list(self.get_payload(datapackage))
        payload = self.backend.get_upload_access(self.config['api_key'],
                                                 self.config['token'],
                                                 pkg.as_dict(), payload)
        success = self.upload(payload)
        return success

    def upload(self, payload):
        """Upload a datapackage to an Open Spending data store."""
        import ipdb;ipdb.set_trace()
        for _file in payload:
            files = {'file': io.open(_file['local'], mode='rb+')}
            response = requests.post(_file['upload_to'], files=files)

    def get_payload(self, datapackage):
        """Return a generator of dict with file info."""
        return (self.get_file_payload(filepath) for
                filepath in self._walker(datapackage))

    def get_file_payload(self, filepath):
        """Return a file payload object."""

        return {
            'local': filepath,
            'name': get_filename(filepath),
            'md5': get_checksum(filepath),
            'length': get_contentlength(filepath)
        }

    def _walker(self, datapackage):
        """Return all files in a datapackage."""
        # TODO: only get files in datapackage, and anything in archive/*
        collected = []
        for root, dirs, files in os.walk(datapackage):
            collected.extend([os.path.join(root, f) for f in files if not f.startswith('.')])
        return collected
