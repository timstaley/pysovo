#pysovo VOEvent Tools
#Convenience functions allowing easy access to information in VOEvent packets. 
#Tim Staley, <timstaley337@gmail.com>, 2012

from lxml import objectify, etree
from astropysics.coords.coordsys import FK5Coordinates
import voeparse

def pull_astro_coords(v):
    """Attempts to determine coordinate system and convert to corresponding
       astropysics class.
    """
    c = voeparse.pull_astro_coords(v)
    if (c.system != voeparse.CoordSystemIDs.fk5
        or c.units != voeparse.CoordUnits.degrees):
        raise ValueError("Unrecognised AstroCoords type")
    return FK5Coordinates(ra=c.ra, dec=c.dec,
                          raerror=c.ra_err, decerror=c.dec_err)
