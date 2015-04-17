# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import io
import hashlib
import base64
from requests_futures.sessions import FuturesSession
from .. import osdatapackage
from .. import _mock
from .. import utilities
from .. import exceptions
from .. import mixins
from .. import compat


def get_filestats(filepath, blocksize=65536):
    """Get stats on a file via iteration over its contents.

    Returns:
    * A tuple of (checksum, length)
    """
    hasher = hashlib.md5()
    length = 0

    with io.open(filepath, mode='r+b') as stream:
        _buffer = stream.read(blocksize)
        while len(_buffer) > 0:
            hasher.update(_buffer)
            as_text = _buffer.decode('utf-8')
            length += len(as_text)
            _buffer = stream.read(blocksize)

    return base64.urlsafe_b64encode(hasher.digest()), compat.str(length)


def get_filename(filepath):
    """Return the actual filename from the filepath."""
    return os.path.basename(filepath)


class Upload(mixins.WithConfig):

    """Upload a datapackage to the flat file store."""

    def __init__(self, config=None):
        super(Upload, self).__init__(config=config)
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
        """Asyncronously upload a datapackage to Open Spending."""

        def _callback(session, response):
            print(response.url)

        session = FuturesSession()
        futures = []
        streams = []
        uploading = True

        for _file in payload:
            headers = {'Content-Length': _file['length'],
                       # 'Content-MD5': _file['md5'],
                       'Content-Type': None,
                       'Connection': None,
                       'User-Agent': None,
                       'Accept-Encoding': None,
                       'Accept': None
            }
            stream = io.open(_file['local'])
            streams.append(stream)
            future = session.put(_file['upload_url'], data=stream,
                                 headers=headers, params=_file['upload_params'],
                                 background_callback=_callback)
            futures.append(future)

        while uploading:
            uploading = not all([future.done() for future in futures])

        for stream in streams:
            stream.close()

    def get_payload(self, datapackage):
        """Return a generator of dict with file info."""
        return (self.get_file_payload(filepath) for
                filepath in self._walker(datapackage))

    def get_file_payload(self, filepath):
        """Return a file payload object."""

        checksum, length = get_filestats(filepath)
        return {
            'local': filepath,
            'name': get_filename(filepath),
            'md5': checksum,
            'length': length
        }

    def _walker(self, datapackage):
        """Return all files in a datapackage."""
        # TODO: only get files in datapackage, and anything in archive/*
        collected = []
        for root, dirs, files in os.walk(datapackage):
            collected.extend([os.path.join(root, f) for f in files if not f.startswith('.')])
        return collected
