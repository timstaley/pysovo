import pysovo.email as email
import pysovo.address_book as address_book 
from astropysics.coords.coordsys import FK5Coordinates 
from observatory import Observatory


chilbolton = Observatory(lat = 51.145762,
                  long = -1.428495,
                  site_altitude = 78,        
                  target_min_elevation = 20, #TO DO: Find out what this should actually be
                  tz = 0,
                  name = "LOFAR-UK (Chilbolton station)",
                  short_name = "Chilbolton",
                  )

#Attributes specific to this particular site:

#Stub function:
chilbolton.check_available = lambda : False #Function that always returns false