from unittest import TestCase
from astropysics.coords.coordsys import FK5Coordinates
import voeparse
from pysovo.utils import convert_voe_coords_to_fk5, reject_swift_bat_trigger
from pysovo.tests.resources import datapaths

class TestCoordConversion(TestCase):
    def test_swift_grb_v2_fk5(self):
        swift_grb_v2 = voeparse.load(datapaths.swift_bat_grb_pos_v2)
        known_swift_grb_posn = FK5Coordinates(ra=74.741200, dec=5.313700,
                                             raerr=0.05, decerr=0.05)
        voe_coords = voeparse.pull_astro_coords(swift_grb_v2)
        fk5 = convert_voe_coords_to_fk5(voe_coords)
        self.assertEqual(fk5, known_swift_grb_posn)
        reject = reject_swift_bat_trigger(swift_grb_v2, fk5)
        self.assertEqual(reject, None)






