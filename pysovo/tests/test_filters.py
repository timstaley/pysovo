from unittest import TestCase
from astropysics.coords.coordsys import FK5Coordinates
import voeparse
from pysovo.utils import convert_voe_coords_to_fk5
from pysovo.filters import reject_swift_bat_trigger
from pysovo.tests.resources import datapaths


def reject_packet(pkt):
    v = voeparse.load(pkt)
    voe_coords = voeparse.pull_astro_coords(v)
    fk5 = convert_voe_coords_to_fk5(voe_coords)
    reject = reject_swift_bat_trigger(v, fk5)
    return reject

class TestSwiftGrbFilters(TestCase):
    def test_good_target(self):
        reject = reject_packet(datapaths.swift_bat_grb_pos_v2)
        self.assertEqual(reject, None)

    def test_low_dec_filter(self):
        reject = reject_packet(datapaths.swift_bat_grb_low_dec)
        self.assertEqual(bool(reject), True)

    def test_lost_lock_filter(self):
        reject = reject_packet(datapaths.swift_bat_grb_lost_lock)
        self.assertEqual(bool(reject), True)

    def test_known_source_filter(self):
        reject = reject_packet(datapaths.swift_bat_known_source)
        self.assertEqual(bool(reject), True)
