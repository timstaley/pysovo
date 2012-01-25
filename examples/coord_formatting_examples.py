#Testing various coord representation libraries

import angles
import ephem

import astropysics.coords.coordsys as ac


print "Comparing entry and display of equatorials:"

ra_deg, dec_deg = 123.2343, -9.53423
astropy_posn = ac.FK5Coordinates(ra_deg, dec_deg)
print "Astropy_posn - default str (hh:mm:ss.sss):", astropy_posn
print "Astropy_posn:", astropy_posn.ra, astropy_posn.dec 
print ""
print "Astropy ami style:", astropy_posn.ra.getHmsStr( canonical=True).replace(":"," ")

print ""
ep_posn1= ephem.Equatorial(str(ra_deg), str(dec_deg))
ep_posn2 = ephem.Equatorial(ephem.degrees(ra_deg), ephem.degrees(dec_deg))
print "Ephem1:", ep_posn1.ra,ep_posn1.dec  
print "Ephem2:", ep_posn2.to_radec()
print "Ephem2 (reformatted):", angles.fmt_angle(ep_posn2.ra), ep_posn2.dec

