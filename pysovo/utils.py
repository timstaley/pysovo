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

def pull_swift_bat_id(voevent):
    if voevent.attrib['ivorn'].find("ivo://nasa.gsfc.gcn/SWIFT#BAT_GRB_Pos") != 0:
        return None
    alert_id = voevent.attrib['ivorn'][len('ivo://nasa.gsfc.gcn/SWIFT#BAT_GRB_Pos_'):]
    alert_id_short = alert_id.split('-')[0]
    return alert_id, alert_id_short

def swift_bool(bstring):
    if bstring == 'true':
        return True
    elif bstring == 'false':
        return False
    else:
        raise ValueError("This string does not appear to be a SWIFT VOEvent "
                          "boolean: %s" % bstring)










