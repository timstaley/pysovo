import unittest

import pysovo as ps
from resources import greenwich

import datetime, pytz
import astropysics

def print_long_short(type, long, short):
    return #Switch off debug prints by uncommenting this line
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
                                        eq_posn=greenwich.never_visible_source,
                                        event_time=greenwich.vernal_equinox_2012,
                                        description="Goodyear blimp",
                                        reason_missed="Out of cheese error")
        print_long_short("event missed", long_msg, short_msg)

class TestObsRequestedFormatting(unittest.TestCase):
    def setUp(self):
        self.time = greenwich.vernal_equinox_2012
        self.site = greenwich.greenwich_site()

    def test_obs_requested_messages(self):
        tests = {"circumpolar": greenwich.circumpolar_north_transit_at_ve_p12hr,
                 "equatorial, on sky": greenwich.equatorial_transiting_at_ve,
                 "equatorial, off sky" : greenwich.equatorial_transiting_at_ve_p12hr}

        for type, posn in tests.iteritems():
            long, short = ps.notifications.obs_requested_message(posn,
                                                                 event_time=self.time,
                                                                 description="flying monkey",
                                                                 obs_site=self.site,
                                                                 current_time=self.time)
            print_long_short(type, long, short)




