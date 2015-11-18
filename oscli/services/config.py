# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import io
import json


FILENAME = '.openspendingrc'
SKELETON = {'api_key': ''}


def locate():
    """Return the path of the active config file, or None.
    """

    # Get pathes
    here = os.getcwd()
    here_path = os.path.join(here, FILENAME)
    home = os.path.expanduser('~')
    home_path = os.path.join(home, FILENAME)

    # Get config path
    if os.path.exists(here_path):
        config_path = here_path
    elif os.path.exists(home_path):
        config_path = home_path
    else:
        config_path = None

    # Return path
    return config_path


def ensure(location='home'):
    """Ensure an valid config file exists; writing one to location if None.
    """

    try:

        # Read and return if exists
        config = read()
        if config is None:
            raise ValueError('No config')
        return config

    except Exception:

        # Get pathes
        here = os.getcwd()
        here_path = os.path.join(here, FILENAME)
        home = os.path.expanduser('~')
        home_path = os.path.join(home, FILENAME)

        # Get config path
        if location == 'here':
            config_path = 'here'
        else:
            config_path = home_path

        # Create and return skeleton
        with io.open(config_path, mode='w+t', encoding='utf-8') as stream:
            stream.write(json.dumps(SKELETON, indent=4))
            stream.seek(0)
            return json.loads(stream.read())


def read():
    """Return the contents of the active config file, or None.
    """

    # Get path
    path = locate()

    try:

        # Return contents
        if path:
            with io.open(path, mode='r+t', encoding='utf-8') as stream:
                return json.loads(stream.read())

    except ValueError:

        # Raise exception if can't read config
        raise ValueError('Config file is not valid')


def write(**data):
    """Write additional data into an active config file.
    """

    # Get and update config
    config = ensure()
    config.update(data)

    # Get config path
    config_path = locate()

    # Write updated config
    with io.open(config_path, mode='w+t', encoding='utf-8') as stream:
        stream.seek(0)
        stream.truncate()
        stream.write(json.dumps(config, indent=4))

    # Return updated config
    return config
