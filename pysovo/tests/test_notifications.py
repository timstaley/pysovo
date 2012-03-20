import unittest
from VOEventLib import VOEvent as voe

import pysovo as ps
import pysovo.observatories.tests.test_data as test_data

import datetime, pytz
import astropysics

def print_long_short(type, long, short):
#    return 
    print
    print "=========================================="
    print "Example {t} messages".format(t=type)
    print "long:"
    print "--------------------------------"
    print long
    print "--------------------------------"
    print "Short:"
    print short
    print "=========================================="
    

        

class TestEventMissedFormatting(unittest.TestCase):
    def test_event_missed_messages(self):
        long_msg, short_msg = ps.notifications.event_missed_message(
                                        eq_posn = test_data.arbitrary_eqpos, 
                                        event_time = test_data.vernal_equinox_2012, 
                                        description = "Goodyear blimp", 
                                        reason_missed = "Out of cheese error")
        print_long_short("event missed", long_msg, short_msg)

class TestObsRequestedFormatting(unittest.TestCase):
    def setUp(self):
        self.time = test_data.vernal_equinox_2012
        self.site = test_data.greenwich()
         
    def test_obs_requested_messages(self):
        tests = {"circumpolar": test_data.circumpolar_north_transit_later, 
                 "equatorial, on sky": test_data.equatorial_on_sky_ve, 
                 "equatorial, off sky" : test_data.equatorial_off_sky_ve}
        
        for type, posn in tests.iteritems():
            long, short = ps.notifications.obs_requested_message(posn, 
                                                                 event_time = self.time,
                                                                 description = "flying monkey",
                                                                 obs_site = self.site,
                                                                 current_time = self.time)
            print_long_short(type, long, short)
        
        
        
        