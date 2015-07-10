import unittest
from pysovo.tests.resources import greenwich
from pysovo.visibility import get_ephem
from pysovo.formatting import datetime_format_long, format_datetime

import jinja2
from jinja2 import Environment, PackageLoader

env = Environment(loader=PackageLoader('pysovo', 'templates'),
                  trim_blocks=True)
env.filters['datetime'] = format_datetime

#--------------------------------------------------------------
basic_site_vis_report = env.get_template('visibility_report.txt')

class TestSiteVisReport(unittest.TestCase):
    def setUp(self):
        self.time = greenwich.vernal_equinox_2012
        self.sites = [greenwich.greenwich_site,
                      greenwich.anti_site]
        self.template = env.get_template('visibility_report.txt')
        def test_tgt(tgt):
#            print "----------------------------"
            print "Target: ", tgt.ra, tgt.dec
#            print
            for site in self.sites:
                vis = get_ephem(tgt, site, self.time)
                site_report = self.template.render(site=site,
                                                   vis=vis,
                                                   dt_style=datetime_format_long)
                print site_report
#            print "----------------------------"

        #Export the function to the test cases:
        self.test_tgt = test_tgt
        print

    def test_never_vis(self):
        self.test_tgt(greenwich.never_visible_source)
    def test_circumpolar(self):
        self.test_tgt(greenwich.circumpolar_north_transit_at_ve_m1hr)
    def test_equatorial_up_now(self):
        self.test_tgt(greenwich.equatorial_transiting_at_ve)
