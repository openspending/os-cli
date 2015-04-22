# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import io
import json


CONFIG_NAME = '.openspendingrc'
CONFIG_SKELETON = {'api_key': ''}


def map_from_string(mapping_string, separate=',', assign='='):

    """Extract a mapping object from a string.

    Args:
        * `mapping_string`: a string with expected mapping format
        * `separate`: separator for properties
        * `assign`: separator for keys, values

    Example:
        * key1=value1,key2=value2

    """

    return dict([arg.split(assign) for arg in mapping_string.split(separate)])


def get_config_path():
    """Return the path of the active config file, or None."""

    here = os.getcwd()
    here_path = os.path.join(here, CONFIG_NAME)
    home = os.path.expanduser('~')
    home_path = os.path.join(home, CONFIG_NAME)

    if os.path.exists(here_path):
        config_path = here_path
    elif os.path.exists(home_path):
        config_path = home_path
    else:
        config_path = None

    return config_path


def read_config():
    """Return the contents of the active config file, or None."""

    _path = get_config_path()

    if _path:
        with io.open(_path, mode='r+t', encoding='utf-8') as stream:
            return json.loads(stream.read())


def locate_config():
    """Return path to active config, or None."""
    return get_config_path()


def write_config(**kwargs):
    """Write data into a config file."""

    _path = get_config_path()

    if _path:
        config_path = _path
    else:
        home = os.path.expanduser('~')
        config_path = os.path.join(home, CONFIG_NAME)

    with io.open(config_path, mode='r+t', encoding='utf-8') as stream:
        config = json.loads(stream.read())

    config.update(kwargs)

    with io.open(config_path, mode='w+t', encoding='utf-8') as stream:
        stream.seek(0)
        stream.truncate()
        stream.write(json.dumps(config))

    return config_path


def ensure_config(location='home'):
    """Ensure an active config file exists; writing one to location if None."""

    here = os.getcwd()
    here_path = os.path.join(here, CONFIG_NAME)
    home = os.path.expanduser('~')
    home_path = os.path.join(home, CONFIG_NAME)

    if location == 'here':
        config_path = 'here'
    else:
        config_path = home_path

    _path = get_config_path()

    if _path:
        with io.open(_path, mode='r+t', encoding='utf-8') as stream:
            return json.loads(stream.read())
    else:
        with io.open(config_path, mode='w+t', encoding='utf-8') as stream:
            stream.write(json.dumps(CONFIG_SKELETON))
            stream.seek(0)
            return json.loads(stream.read())

def is_datapackage(_path):
    """Ensure that _path is a Data Package."""

    descriptor_name = 'datapackage.json'

    if not os.path.isdir(_path):
        MSG = ('The path is not a directory, and therefore not a valid '
               'Data Package.')
        return False, MSG

    descriptor = os.path.join(_path, descriptor_name)
    if not os.path.exists(descriptor):
        MSG = ('The directory does not include a {0}, and so is not a valid '
               'Data Package.'.format(descriptor_name))
        return False, MSG

    MSG = ('The path is a valid Data Package')
    return True, MSG
