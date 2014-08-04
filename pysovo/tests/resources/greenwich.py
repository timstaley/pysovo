#pysovo VOEvent Tools
#Tim Staley, <timstaley337@gmail.com>, 2012
from __future__ import absolute_import
import datetime, pytz
import ephem
from pysovo.visibility import DEG_PER_RADIAN
"""An example obs_site initialization, with equatorial positions of known
transit time, etc, for unit testing purposes."""

# from astropysics.coords.coordsys import ephem.Equatorial
# import astropysics.obstools

#---------------------------------------------------------------------------
#Test data:

greenwich_site = ephem.Observer()
greenwich_site.lat = 51.5/DEG_PER_RADIAN
greenwich_site.long = 0
greenwich_site.name = "Greenwich"
greenwich_site.horizon = 0



anti_site = ephem.Observer()
anti_site.lat = -38.5/DEG_PER_RADIAN
anti_site.long = 0
anti_site.name = "Antipodean"
anti_site.horizon = 0


vernal_equinox_2012 = datetime.datetime(2012, 03, 20,
                                           5, 14,
                                           tzinfo=pytz.utc)

vernal_equinox_2012_p12h = vernal_equinox_2012 + datetime.timedelta(hours=12)


#Greenwich LST at V.E. (h:m:s) = 17:6:32  approx
greenwish_lst_at_ve = 17.1096992 #decimal hours
#12 hours later:
greenwish_lst_at_ve_p12h = 5.1425530145722549


##NB this is approximately zenith at the 2012 vernal equinox (at greenwich):
equatorial_transiting_at_ve = ephem.Equatorial("17:6:32", "+0.0", epoch=ephem.J2000)
equatorial_transiting_at_ve_p12hr = ephem.Equatorial("5:6:32", "+0.0", epoch=ephem.J2000)
equatorial_transiting_at_ve_m1hr = ephem.Equatorial("16:6:32", "+0.0", epoch=ephem.J2000)

#NB, this one sets the day after VE.
equatorial_transiting_at_ve_p13hr = ephem.Equatorial("6:6:32", "+0.0", epoch=ephem.J2000)

equatorial_transiting_at_ve_m5hr = ephem.Equatorial("12:6:32", "+0.0", epoch=ephem.J2000)

#NB, this has not set from yesterdays transit at VE.
equatorial_transiting_at_ve_m6hr = ephem.Equatorial("11:6:32", "+0.0", epoch=ephem.J2000)

circumpolar_north_transit_at_ve_m1hr = ephem.Equatorial("16:6:32", " +89.0", epoch=ephem.J2000)
circumpolar_north_transit_at_ve = ephem.Equatorial("17:6:32", " +89.0", epoch=ephem.J2000)
circumpolar_north_transit_at_ve_p12hr = ephem.Equatorial("5:6:32", "+89.0", epoch=ephem.J2000)

never_visible_source = ephem.Equatorial("17:6:32", "-70.0", epoch=ephem.J2000)
#---------------------------------------------------------------------------
