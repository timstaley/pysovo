#pysovo VOEvent Tools 
#Tim Staley, <timstaley337@gmail.com>, 2012

import datetime, pytz
import unittest

"""An example obs_site initialization, with equatorial positions of known
transit time, etc, for unit testing purposes."""

from astropysics.coords.coordsys import FK5Coordinates
import astropysics.obstools

#---------------------------------------------------------------------------
#Test data: 

greenwich_site = astropysics.obstools.Site(lat=51.5,
                                       long=0,
                                        alt=0,
                                        tz=0,
                                        name="Greenwich"
                                        )
greenwich_site.target_min_elevation = 0
greenwich_site.long_name = "Royal Greenwich Observatory"


#def antipodean_site():
anti_site = astropysics.obstools.Site(lat= -38.5,
                                       long=180,
                                        alt=0,
                                        tz=12,
                                        name="Antipodean"
                                        )
anti_site.target_min_elevation = 0
anti_site.long_name = "Antipodean Observatory"


vernal_equinox_2012 = datetime.datetime(2012, 03, 20,
                                           5, 14,
                                           tzinfo=pytz.utc)

vernal_equinox_2012_p12h = vernal_equinox_2012 + datetime.timedelta(hours=12)


#Greenwich LST at V.E. (h:m:s) = 17:6:32  approx
greenwish_lst_at_ve = 17.1096992 #decimal hours
#12 hours later:
greenwish_lst_at_ve_p12h = 5.1425530145722549


##NB this is approximately zenith at the 2012 vernal equinox (at greenwich):
equatorial_transiting_at_ve = FK5Coordinates("17:6:32 +0.0 J2000.0")
equatorial_transiting_at_ve_p12hr = FK5Coordinates("5:6:32 +0.0 J2000.0")
equatorial_transiting_at_ve_m1hr = FK5Coordinates("16:6:32 +0.0 J2000.0")

#NB, this one sets the day after VE.
equatorial_transiting_at_ve_p13hr = FK5Coordinates("6:6:32 +0.0 J2000.0")

equatorial_transiting_at_ve_m5hr = FK5Coordinates("12:6:32 +0.0 J2000.0")

#NB, this has not set from yesterdays transit at VE.
equatorial_transiting_at_ve_m6hr = FK5Coordinates("11:6:32 +0.0 J2000.0")

circumpolar_north_transit_at_ve_m1hr = FK5Coordinates("16:6:32 +89.0 J2000.0")
circumpolar_north_transit_at_ve = FK5Coordinates("17:6:32 +89.0 J2000.0")
circumpolar_north_transit_at_ve_p12hr = FK5Coordinates("5:6:32 +89.0 J2000.0")

never_visible_source = FK5Coordinates("17:6:32 -70.0 J2000.0")
#---------------------------------------------------------------------------
