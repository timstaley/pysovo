from unittest import TestCase
import voeparse as vp
from pysovo.tests.resources import datapaths
import pysovo.voevent as vo_subs
import datetime

class TestFollowupVoevent(TestCase):
    def test_initial_case(self):
        with open(datapaths.swift_bat_grb_pos_v2) as f:
            swift_alert = vp.load(f)

        request_status = {'sent_time':datetime.datetime.utcnow(),
                          'acknowledged':False,
                          }

        v = vo_subs.create_ami_followup_notification(swift_alert,
                                                 stream_id=001,
                                                 request_status=request_status)
        vp.assert_valid_as_v2_0(v)
        with open('/tmp/test_voevent.xml', 'w') as f:
            vp.dump(v, f)
