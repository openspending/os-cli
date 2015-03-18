# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import io
import json
import shutil


def persist_datapackage(descriptor, datapackage_path, data_paths, archive_paths):

    """Persist a Data Package to a local location or remote file storage.

    Args:
        * `descriptor`: datapackage as dict
        * `datapackage_path`: path for writing this data package
        * `data_paths`: list of resources to write into data directory
        * `archive_paths`: list of file paths to write into archive directory

    """

    descriptor_file = os.path.join(datapackage_path, 'datapackage.json')
    data_dir = os.path.join(datapackage_path, 'data')
    archive_dir = os.path.join(datapackage_path, 'archive')

    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir)

    with io.open(descriptor_file, mode='w+t', encoding='utf-8') as dest:
        dest.write(json.dumps(descriptor, ensure_ascii=False, indent=4))

    for filepath in data_paths:
        shutil.copy2(filepath, data_dir)

    for filepath in archive_paths:
        shutil.copy2(filepath, archive_dir)

    return True
