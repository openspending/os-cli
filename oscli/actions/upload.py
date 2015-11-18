# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import io
import hashlib
import base64
import requests
from requests_futures.sessions import FuturesSession
from .. import helpers, services, compat


class Upload(object):
    """Upload a datapackage to the flat file store.

    Args:
        path (str): Path to the datapackage dir.
    """

    # Public

    def __init__(self, path):
        self.path = path
        self.config = services.config.read()
        with open(os.path.join(self.path, 'datapackage.json')) as file:
            self.descriptor = json.load(file)

    def run(self):
        """Run the upload flow.
        """
        req_payload = self.__get_payload()
        res_payload = self.__authorize(res_payload)
        self.__upload(res_payload)

    # Private

    def __get_payload(self):
        """Get datapackage payload.
        """

        # Initial payload
        payload = {
            'metadata': {
                'name': self.descriptor['name'],
                'owner': self.descriptor['owner'],
            },
            'filedata': {},
        }

        # Fill filedata
        for root, dirs, files in os.walk(self.path):
            for path in files:
                name = os.path.basename(path)
                if name.startswith('.'):
                    continue
                abspath = os.path.join(root, path)
                length = os.path.getsize(abspath)
                md5 = helpers.get_checksum(abspath)
                payload['filedata'][path] = {
                    'name': name,
                    'length': length,
                    'md5': md5,
                }

        # Return payload
        return payload

    def __authorize(self, payload):
        """Authorize payload to upload to Open Spending.
        """

        # Make request
        res = requests.post(
                self.config['authz_url'] + 'datastore/',
                headers={'API-Key': self.config['api-key']},
                data=json.dumps(payload))

        # Return authorized payload
        return json.loads(res.data)

    def __upload(self, filedata):
        """Asyncronously upload a datapackage to Open Spending.
        """

        # Prepare
        session = FuturesSession()
        futures = []
        streams = []
        uploading = True

        # Start uploading
        for file in payload:
            headers = {
                'Content-Length': file['length'],
                'Content-MD5': file['md5'],
                'Content-Type': None,
                'Connection': None,
                'User-Agent': None,
                'Accept-Encoding': None,
                'Accept': None,
            }
            stream = io.open(file['local'])
            streams.append(stream)
            future = session.put(
                    file['upload_url'],
                    data=stream,
                    headers=headers,
                    params=file['upload_params'],
                    background_callback=self.__notify)
            futures.append(future)

        # Wait for uploads
        while uploading:
            uploading = not all([future.done() for future in futures])

        # Close streams
        for stream in streams:
            stream.close()

    def __nofify(session, response):
        """Notify about uploading to Open Spending.
        """
        parsed = compat.parse.urlparse(response.url)
        url = '{0}://{1}{2}'.format(parsed.scheme, parsed.netloc, parsed.path)
        status = response.status_code
        if status == 200:
            text = ('This file is now serving live Open Spending.')
        else:
            text = ('Something went wrong with this file. Here is '
                    'some data we received.\n\n{0}'.format(response.text))
        print('FILE (status {0}): {1}\n'.format(status, url, text))
