"""
Misc. convenience routines.
"""

import os
from collections import Sequence
from astropysics.coords.coordsys import FK5Coordinates
import voeparse

def listify(x):
    """
    Returns [x] if x is not already a list.

    Used to make functions accept either scalar or array inputs -
    simply `listify` a variable to make sure it's in list format.
    """
    if (not isinstance(x, basestring)) and isinstance(x, Sequence):
        return x
    else:
        return [x]

def ensure_dir(filename):
    """Ensure parent directory exists, so you can write to `filename`."""
    d = os.path.dirname(filename)
    if not os.path.exists(d):
        os.makedirs(d)


def convert_voe_coords_to_fk5(c):
    """Unit-checked conversion from voeparse.Position2D -> astropysics FK5"""
    if (c.system != voeparse.sky_coord_system.fk5
        or c.units != 'deg'):
        raise ValueError("Unrecognised Coords type: %s, %s" % (c.system, c.units))
    return FK5Coordinates(ra=c.ra, dec=c.dec,
                          raerror=c.err, decerror=c.err)









