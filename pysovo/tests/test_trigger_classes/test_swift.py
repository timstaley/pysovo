from unittest import TestCase
from astropysics.coords.coordsys import FK5Coordinates
import voeparse
from pysovo.utils import convert_voe_coords_to_fk5
from pysovo.triggers import swift
from pysovo.tests.resources import datapaths

class TestSwiftGrbFilters(TestCase):
    def setUp(self):
        def reject_packet(pkt):
            with open(pkt) as f:
                v = voeparse.load(f)
            alert = swift.BatGrb(v)
            return alert.reject()
        self.reject = reject_packet

    def test_good_target(self):
        self.assertIsNone(self.reject(datapaths.swift_bat_grb_pos_v2))

    def test_lost_lock_filter(self):
        self.assertIsNotNone(self.reject(datapaths.swift_bat_grb_lost_lock))

    def test_known_source_filter(self):
        self.assertIsNotNone(self.reject(datapaths.swift_bat_known_source))

class TestBatGrbClass(TestCase):
    def test_init(self):
        with open(datapaths.swift_bat_grb_pos_v2) as f:
            trigger = swift.BatGrb(voeparse.load(f))
