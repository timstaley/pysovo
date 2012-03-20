from pysovo.observatories import observatory
import datetime, pytz
import astropysics

#---------------------------------------------------------------------------------------------------------
def greenwich():
    return observatory.Observatory(lat=51.5,
                                    long=0,
                                    site_altitude=0,
                                    tz=0,
                                    name="Not really - this is a test",
                                    short_name="Greenwich"
                                    )
    
vernal_equinox_2012 = datetime.datetime(2012, 03, 20,
                                           5, 14,
                                           tzinfo = pytz.utc)

equatorial_on_sky_ve = astropysics.coords.coordsys.FK5Coordinates("17:6:32 +0.0 J2000.0")
equatorial_off_sky_ve = astropysics.coords.coordsys.FK5Coordinates("5:6:32 +0.0 J2000.0")

circumpolar_north_transit_at_ve = astropysics.coords.coordsys.FK5Coordinates("17:6:32 +89.0 J2000.0")
circumpolar_north_transit_later = astropysics.coords.coordsys.FK5Coordinates("5:6:32 +89.0 J2000.0")

southern_hemisphere = astropysics.coords.coordsys.FK5Coordinates("5:6:32 -60.0 J2000.0")

#---------------------------------------------------------------------------------------------------------
arbitrary_eqpos = astropysics.coords.coordsys.FK5Coordinates("12:6:32 +45.0 J2000.0")
