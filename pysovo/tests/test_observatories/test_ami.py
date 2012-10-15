import unittest
import pysovo

from pysovo.observatories import ami
from pysovo.observatories import ami_module
from pysovo.tests.resources import datapaths

from datetime import timedelta
from astropysics.coords.coordsys import FK5Coordinates

class TestAMIRequestMethod(unittest.TestCase):

    def setUp(self):
        def dummy_func(request_info, local_config):
            pass
#            local_config.unit_test_data = request_info
        ami.internal_request_mechanism = dummy_func
        ami.default_action = "CHECK"

        self.voevent = pysovo.voevent.build.from_file(
                                              datapaths.swift_bat_grb_pos_v2)
        self.config = pysovo.LocalConfig()

    def test_coord_formatting(self):
        known_results = {
         FK5Coordinates(ra=270, dec=57.5):('18 0 00.00', '57 30 00.00'),
         FK5Coordinates("17:6:32 +57.5 J2000.0"): ('17 6 32.00', '57 30 00.00'),
         FK5Coordinates("17:06:32.01 -12.22 J2000.0"): ('17 6 32.01', '-12 13 12.00'),
         FK5Coordinates("17:06:32.0099 -12.22 J2000.0"): ('17 6 32.01', '-12 13 12.00'),
                         }

        for coords, ami_string in known_results.iteritems():
            converted = ami_module.format_ami_coords(coords)
#            print "\nPosn:", coords
#            print 'RA string:"' + converted[0] + '"'
#            print 'DEC string:"' + converted[1] + '"'
            self.assertEqual(converted, ami_string)

    def test_duration_formatting(self):
        """test_duration_formatting
        
        Should return in format hh.mm
        """
        known_results = {timedelta(minutes=25): "00.25",
                         timedelta(minutes=25.9999): "00.25",
                         timedelta(hours=2.5): "02.30",
                         timedelta(hours=1): "01.00",
                         timedelta(hours=10.5): "10.30",
                         }
        for t, s in known_results.iteritems():
            self.assertEqual(ami_module.format_ami_duration(t),
                             s)


    def test_formatting_does_not_throw(self):
        observation_text = ami.request_observation(
                                   pysovo.voevent.pull_astro_coords(self.voevent),
                                   "swift_grb",
                                   self.voevent,
                                   self.config)

#        print
#        print "Sample AMI request body text:"
#        print observation_text


