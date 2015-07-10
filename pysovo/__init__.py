from __future__ import absolute_import


import pysovo.comms
import pysovo.visibility
import pysovo.filters
import pysovo.formatting
import pysovo.triggers
import pysovo.utils
import pysovo.voevent
import socket

from ._version import get_versions
__versiondict__ = get_versions()
__version__ = __versiondict__['version']
del get_versions


def base_context():
    """
    Get a dictionary of context variables used across multiple templates.
    """
    hostname = socket.gethostname()
    return dict(
        versions=__versiondict__,
        hostname=hostname,
        dt_style=pysovo.formatting.datetime_format_long
    )