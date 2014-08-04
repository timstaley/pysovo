from __future__  import absolute_import
from unittest import TestCase
import voeventparse
from pysovo.utils import convert_voe_coords_to_eqposn
from pysovo.tests.resources import datapaths
from pysovo.visibility import DEG_PER_RADIAN
import ephem

class TestCoordConversion(TestCase):
    def test_swift_grb_v2_fk5(self):
        with open(datapaths.swift_bat_grb_pos_v2) as f:
            swift_grb_v2 = voeventparse.load(f)
        known_swift_grb_posn = ephem.Equatorial(
            74.741200/DEG_PER_RADIAN, 25.313700/DEG_PER_RADIAN,
            epoch=ephem.J2000)
        voe_coords = voeventparse.pull_astro_coords(swift_grb_v2)
        extracted_posn = convert_voe_coords_to_eqposn(voe_coords)
        self.assertEqual(extracted_posn.ra, known_swift_grb_posn.ra)
        self.assertEqual(extracted_posn.dec, known_swift_grb_posn.dec)


