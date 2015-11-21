# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import io
import json
from .. import compat


SKELETON = {'api_key': ''}
FILENAME = '.openspendingrc'
HEREPATH = os.path.join(os.getcwd(), FILENAME)
HOMEPATH = os.path.join(os.path.expanduser('~'), FILENAME)
DEFAULTPATH = os.path.join(os.path.dirname(__file__), '..', 'config.json')


def locate():
    """Return the path of the active config file, or None.
    """

    # Get config path
    if os.path.exists(HEREPATH):
        path = HEREPATH
    elif os.path.exists(HOMEPATH):
        path = HOMEPATH
    else:
        path = None

    # Return path
    return path


def ensure():
    """Ensure config file exists; writing one to $HOME if None.
    """

    # Get path
    path = locate()

    # Need to create
    if not path:
        path = HOMEPATH
        with io.open(path, 'w', encoding='utf-8') as file:
            file.write(compat.str(json.dumps(SKELETON, indent=4)))

    # Return path
    return path


def read(add_default=True):
    """Return the contents of the active config.
    """

    # Get path
    path = locate()

    # Init config
    config = {}

    # Default config
    if add_default:
        with io.open(DEFAULTPATH, encoding='utf-8') as file:
            config.update(json.loads(file.read()))

    # User config
    if path:
        with io.open(path, encoding='utf-8') as file:
            contents = file.read()
            if contents:
                try:
                    config.update(json.loads(contents))
                except Exception:
                    raise ValueError('Config file is not valid')

    # Return merged
    return config


def write(**data):
    """Write additional data into an active config file.
    """

    # Get and update config
    ensure()
    config = read(add_default=False)
    config.update(data)

    # Get config path
    path = locate()

    # Write updated config
    with io.open(path, 'w', encoding='utf-8') as file:
        file.write(json.dumps(config, indent=4))

    # Return updated config
    config = read()
    return config
