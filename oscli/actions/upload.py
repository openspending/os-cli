# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import io
import json
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
        res_payload = self.__authorize(req_payload)
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
            for name in files:
                if name.startswith('.'):
                    continue
                fullpath = os.path.join(root, name)
                path = os.path.relpath(fullpath, self.path)
                md5, length = helpers.get_filestats(fullpath)
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
                self.config['authz_url'],
                headers={'API-Key': self.config.get('api_key', '')},
                data=json.dumps(payload))

        # Return authorized payload
        return res.json()

    def __upload(self, payload):
        """Asyncronously upload a datapackage to Open Spending.
        """

        # Prepare
        session = FuturesSession()
        futures = []
        streams = []
        uploading = True

        # Start uploading
        for path, file in payload['filedata'].items():
            fullpath = os.path.join(self.path, path)
            headers = {
                'Content-Length': file['length'],
                'Content-MD5': file['md5'],
            }
            stream = io.open(fullpath)
            streams.append(stream)
            future = session.put(
                    file['upload_url'],
                    data=stream,
                    headers=headers,
                    params=file['upload_query'],
                    background_callback=self.__notify)
            futures.append(future)

        # Wait for uploads
        while uploading:
            uploading = not all([item.done() for item in futures])

        # Close streams
        for stream in streams:
            stream.close()

    def __notify(self, session, response):
        """Notify about uploading to Open Spending.
        """

        # Prepare message
        status = response.status_code
        if status == 200:
            msg = ('This file is now serving live Open Spending.')
        else:
            msg = ('Something went wrong with this file. Here is '
                   'some data we received.\n\n{0}'.format(response.text))

        # Prepare url
        parsed = compat.parse.urlparse(response.url)
        url = '{0}://{1}{2}'.format(parsed.scheme, parsed.netloc, parsed.path)

        # Print file status
        print('FILE (status {0}): {1}'.format(status, url, msg))
