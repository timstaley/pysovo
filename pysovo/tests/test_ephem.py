from __future__ import absolute_import
import unittest
from pysovo.tests.resources import greenwich
import pysovo.visibility as vis
from pysovo.visibility import TargetStatusKeys as tkeys
from pysovo.visibility import DEG_PER_RADIAN


class TestPyEphemSiteVisibilityCalcs(unittest.TestCase):
    def setUp(self):
        self.time = greenwich.vernal_equinox_2012
        self.site = greenwich.greenwich_site
        self.target = greenwich.equatorial_transiting_at_ve

    def test_status(self):
        test_cases = {"circumpolar": greenwich.circumpolar_north_transit_at_ve_p12hr,
                 "equatorial, on sky": greenwich.equatorial_transiting_at_ve,
                 "equatorial, off sky" : greenwich.equatorial_transiting_at_ve_p12hr,
                 "never": greenwich.never_visible_source}

    def test_always_visible(self):
        target = greenwich.circumpolar_north_transit_at_ve
        e = vis.get_ephem(target,
                                    self.site, self.time)
        self.assertEqual(e[tkeys.type], 'always')
        self.assertEqual(e[tkeys.visible_now], True)

        target_polar_offset = (90 - target.dec*DEG_PER_RADIAN)
        self.assertAlmostEqual(e[tkeys.trans_pos][0],
                               self.site.lat*DEG_PER_RADIAN + target_polar_offset,
                               places=1)


    def test_never_visible(self):
        e = vis.get_ephem(greenwich.never_visible_source,
                                    self.site, self.time)
        self.assertEqual(e[tkeys.type], 'never')
        self.assertEqual(e[tkeys.visible_now], False)

    def test_sometimes_visible(self):
        now = vis.get_ephem(greenwich.equatorial_transiting_at_ve,
                                    self.site, self.time)
        later = vis.get_ephem(greenwich.equatorial_transiting_at_ve_p12hr,
                                    self.site, self.time)
        self.assertEqual(now[tkeys.type], 'sometimes')
        self.assertEqual(now[tkeys.visible_now], True)

        self.assertEqual(later[tkeys.type], 'sometimes')
        self.assertEqual(later[tkeys.visible_now], False)

        print
        print now[tkeys.current_pos]
        print now[tkeys.trans_pos]
        print later[tkeys.current_pos]
        print later[tkeys.trans_pos]



