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
        descrpath = os.path.join(self.path, 'datapackage.json')
        with io.open(descrpath, encoding='utf-8') as file:
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

        # Allowed paths
        allowed_paths = ['archive', 'scripts', 'datapackage.json']
        for resource in self.descriptor['resources']:
            path = resource.get('path')
            if path:
                allowed_paths.append(path)

        # Fill filedata
        for root, dirs, files in os.walk(self.path):
            for name in files:
                if name.startswith('.'):
                    continue
                fullpath = os.path.join(root, name)
                path = os.path.relpath(fullpath, self.path)
                allowed = False
                for allowed_path in allowed_paths:
                    if path.startswith(allowed_path):
                        allowed = True
                if not allowed:
                    continue
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
        responses = []
        futures = []
        files = []

        # Start uploading
        for path, metadata in payload['filedata'].items():
            fullpath = os.path.join(self.path, path)
            headers = {
                'Content-Length': metadata['length'],
                'Content-MD5': metadata['md5'],
            }
            file = io.open(fullpath, mode='rb')
            files.append(file)
            future = session.put(
                    metadata['upload_url'],
                    data=file,
                    headers=headers,
                    params=metadata['upload_query'],
                    background_callback=self.__notify)
            futures.append(future)

        # Wait uploading
        for future in futures:
            exception = future.exception()
            if exception:
                raise exception
            response = future.result()
            responses.append(response)

        # Raise if errors
        for response in responses:
            if response.status_code != 200:
                url = self.__clean_url(response.url)
                message = (
                    'Something went wrong with "%s" file.\n\n'
                    'Here is response we\'ve received:\n\n%s' %
                    (url, response.text))
                raise RuntimeError(message)

        # Close files
        for file in files:
            file.close()

    def __notify(self, session, response):
        """Notify about uploading to Open Spending.
        """
        url = self.__clean_url(response.url)
        print('FILE (status %s): %s' % (response.status_code, url))

    def __clean_url(self, url):
        """Remove from url query string etc.
        """
        parsed = compat.parse.urlparse(url)
        url = '{0}://{1}{2}'.format(parsed.scheme, parsed.netloc, parsed.path)
        return url
