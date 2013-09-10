from unittest import TestCase
from astropysics.coords.coordsys import FK5Coordinates
import voeparse
from pysovo.utils import convert_voe_coords_to_fk5
import pysovo.filters as filters
from pysovo.tests.resources import datapaths

class TestAmiTargetFilters(TestCase):
    def test_low_dec(self):
        good_src = voeparse.load(datapaths.swift_bat_grb_pos_v2)
        bad_src = voeparse.load(datapaths.swift_bat_grb_low_dec)

        good_fk5 = convert_voe_coords_to_fk5(
                                     voeparse.pull_astro_coords(good_src))
        bad_fk5 = convert_voe_coords_to_fk5(
                                     voeparse.pull_astro_coords(bad_src))
        self.assertIsNone(filters.ami.reject(good_fk5))
        self.assertIsNotNone(filters.ami.reject(bad_fk5))
