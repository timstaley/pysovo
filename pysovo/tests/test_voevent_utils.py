import unittest
from unittest import TestCase
from astropysics.coords.coordsys import FK5Coordinates
import pysovo.voevent_utils
import voeparse
from .resources import datapaths
from pysovo import voevent_utils

class TestCoordConversion(TestCase):
    def test_swift_grb_v2_fk5(self):
        swift_grb_v2 = voeparse.load(datapaths.swift_bat_grb_pos_v2)
        known_swift_grb_posn = FK5Coordinates(ra=74.741200, dec= -9.313700,
                                             raerr=0.05, decerr=0.05)
        p = voevent_utils.pull_astro_coords(swift_grb_v2)
        self.assertEqual(p, known_swift_grb_posn)






