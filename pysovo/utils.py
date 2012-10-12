#pysovo VOEvent Tools
#Tim Staley, <timstaley337@gmail.com>, 2012

from astropysics.coords.coordsys import FK5Coordinates
import os
from collections import Sequence

def listify(x):
    """
    Returns [x] if x is not already a list.
    
    Used to make functions accept either scalar or array inputs - 
    simply `listify` a variable to make sure it's in list format.
    """
    if (not isinstance(x, str)) and isinstance(x, Sequence):
        return x
    else:
        return [x]

def ensure_dir(filename):
    """Ensure parent directory exists, so you can write to `filename`."""
    d = os.path.dirname(filename)
    if not os.path.exists(d):
        os.makedirs(d)









