import unittest
from pysovo.tests.resources import greenwich
import pysovo.notify as notify

from pysovo.notify import TargetStatusKeys as tkeys

class TestSiteReportCalcs(unittest.TestCase):
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
#            for k2, v2 in notify.site_report(v, self.site, self.time).iteritems():
#                print k2, ":", str(v2)

    def test_always_visible(self):
        e = notify.site_report(greenwich.circumpolar_north_transit_at_ve,
                                    self.site, self.time)
        self.assertEqual(e[tkeys.type], 'always')

    def test_never_visible(self):
        e = notify.site_report(greenwich.never_visible_source,
                                    self.site, self.time)
        self.assertEqual(e[tkeys.type], 'never')

class TestEmptyDisplay(unittest.TestCase):
    def test_empty(self):
        target = {'position':greenwich.circumpolar_north_transit_at_ve,
                'description':'UFO'}
        print "\n**************************"
        print notify.long_template.render(target=target,
                                          note_time=greenwich.vernal_equinox_2012,
                                          dt_style=notify.datetime_format_long)

class TestSiteReportDisplay(unittest.TestCase):
    def setUp(self):
        self.time = greenwich.vernal_equinox_2012
        self.sites = [greenwich.greenwich_site,
                      greenwich.anti_site]
        def test_tgt(tgt):
            tgt_dict = {'position': tgt, 'description': 'test event'}
            print "\n**************************"
            print notify.generate_report_text(tgt_dict, self.sites, self.time)
        self.test_tgt = test_tgt

    def test_never_vis(self):
        self.test_tgt(greenwich.never_visible_source)
    def test_circumpolar(self):
        self.test_tgt(greenwich.circumpolar_north_transit_at_ve_m1hr)
    def test_equatorial_up_now(self):
        self.test_tgt(greenwich.equatorial_transiting_at_ve)


#    def test_obs_requested_messages(self):
#        tests = {"circumpolar": greenwich.circumpolar_north_transit_at_ve_p12hr,
#                 "equatorial, on sky": greenwich.equatorial_transiting_at_ve,
#                 "equatorial, off sky" : greenwich.equatorial_transiting_at_ve_p12hr}
#
#        for type, posn in tests.iteritems():
#            long, short = ps.notifications.obs_requested_message(posn,
#                                                                 event_time=self.time,
#                                                                 description="flying monkey",
#                                                                 obs_site=self.site,
#                                                                 current_time=self.time)
#
class TestActionsDisplay(unittest.TestCase):
    def test_action(self):
        target = {'position':greenwich.circumpolar_north_transit_at_ve,
                'description':'UFO'}
        actions = ["Observation requested from AMI."]
        print "\n**************************"
        print notify.long_template.render(target=target,
                                          note_time=greenwich.vernal_equinox_2012,
                                          dt_style=notify.datetime_format_long,
                                          actions_taken=actions)

