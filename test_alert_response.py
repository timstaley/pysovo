
import sys
from VOEventLib import VOEvent as voe, Vutil as voe_utils
from pysovo import email_alerts, observatories, utils

import alert_response

test_packet = voe_utils.parse("test_data/BAT_GRB_Pos_512035-500.xml")

alert_response.swift_bat_grb_logic(test_packet)

 