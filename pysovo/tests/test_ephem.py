import unittest
from pysovo.tests.resources import greenwich
import pysovo.ephem as ephem

from pysovo.ephem import TargetStatusKeys as tkeys

class TestSiteVisibilityCalcs(unittest.TestCase):
    def setUp(self):
        self.time = greenwich.vernal_equinox_2012
        self.site = greenwich.greenwich_site
        self.target = greenwich.equatorial_transiting_at_ve

    def test_status(self):
        test_cases = {"circumpolar": greenwich.circumpolar_north_transit_at_ve_p12hr,
                 "equatorial, on sky": greenwich.equatorial_transiting_at_ve,
                 "equatorial, off sky" : greenwich.equatorial_transiting_at_ve_p12hr,
                 "never": greenwich.never_visible_source}

#        print
#        for k, v in test_cases.iteritems():
#            print "-------------"
#            print k, ":"
#            for k2, v2 in notify.visibility(v, self.site, self.time).iteritems():
#                print k2, ":", str(v2)

    def test_always_visible(self):
        e = ephem.visibility(greenwich.circumpolar_north_transit_at_ve,
                                    self.site, self.time)
        self.assertEqual(e[tkeys.type], 'always')

    def test_never_visible(self):
        e = ephem.visibility(greenwich.never_visible_source,
                                    self.site, self.time)
        self.assertEqual(e[tkeys.type], 'never')

    def test_sometimes_visible(self):
        now = ephem.visibility(greenwich.equatorial_transiting_at_ve,
                                    self.site, self.time)
        later = ephem.visibility(greenwich.equatorial_transiting_at_ve_p12hr,
                                    self.site, self.time)
        self.assertEqual(now[tkeys.type], 'sometimes')
        self.assertEqual(later[tkeys.type], 'sometimes')



