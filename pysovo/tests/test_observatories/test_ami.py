import unittest
from astropysics.coords.coordsys import FK5Coordinates
import voeparse
from datetime import timedelta

from pysovo.tests.resources import datapaths
from pysovo.observatories import ami


class TestRequestFormatting(unittest.TestCase):
    def setUp(self):
        self.voevent = voeparse.load(datapaths.swift_bat_grb_pos_v2)

    def test_coord_formatting(self):
        known_results = {
         FK5Coordinates(ra=270, dec=57.5):('18 0 00.00', '57 30 00.00'),
         FK5Coordinates("17:6:32 +57.5 J2000.0"): ('17 6 32.00', '57 30 00.00'),
         FK5Coordinates("17:06:32.01 -12.22 J2000.0"): ('17 6 32.01', '-12 13 12.00'),
         FK5Coordinates("17:06:32.0099 -12.22 J2000.0"): ('17 6 32.01', '-12 13 12.00'),
                         }

        for coords, ami_strings in known_results.iteritems():
            converted = (ami._format_fk5_to_ami_ra(coords),
                         ami._format_fk5_to_ami_dec(coords))
#            print "\nPosn:", coords
#            print 'RA string:"' + converted[0] + '"'
#            print 'DEC string:"' + converted[1] + '"'
            self.assertEqual(converted, ami_strings)

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
            self.assertEqual(ami._format_timedelta_to_ami_duration(t), s)


    def test_full_formatting(self):
        dummy_coords = FK5Coordinates(ra=270, dec=57.5)
        good_args = dict(target_coords=dummy_coords,
                            target_name='Betelgeuse',
                            timing='ASAP',
                            action='CHECK',
                            requester='BOB',
                            duration=timedelta(hours=3.14),
                            comment="Rhubarb rhubarb rhubarb.",
                            array='AMI-LA')

        obs_text = ami._typeset_obs_request_email(**good_args)

        print
        print "Sample AMI request body text:"
        print obs_text
        bad_args = good_args.copy()
        bad_args['timing'] = 'FUBAR'
        with self.assertRaises(ValueError):
                ami._typeset_obs_request_email(**bad_args)

        bad_args = good_args.copy()
        bad_args['action'] = 'FUBAR'
        with self.assertRaises(ValueError):
                ami._typeset_obs_request_email(**bad_args)
