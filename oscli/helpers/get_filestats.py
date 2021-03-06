# -*- coding: utf-8 -*-
import io
import base64
import hashlib
from .. import compat


def get_filestats(filepath, blocksize=65536):
    """Get stats on a file via iteration over its contents.

    Returns:
        (str, str) A tuple of (md5, length)
    """

    # Prepare hasher
    hasher = hashlib.md5()
    length = 0

    # Iterate over file
    with io.open(filepath, mode='rb') as stream:
        chunk = stream.read(blocksize)
        while len(chunk) > 0:
            hasher.update(chunk)
            length += len(chunk)
            chunk = stream.read(blocksize)

    # Encode md5, stringify length
    md5 = base64.b64encode(hasher.digest()).decode('utf-8')
    length = compat.str(length)

    # Return results
    return md5, length
