import unittest
from VOEventLib import VOEvent as voe

import pysovo
from pysovo.observatories import ami

import test_data

import datetime, pytz
import astropysics

class TestAMIRequestMethod(unittest.TestCase):
    def setUp(self):
        
        def dummy_func(request_info, local_config):
            pass
        ami.internal_request_mechanism = dummy_func
        ami.default_action = "CHECK" 
        
        v = voe.VOEvent(version="2.0")
        v.set_ivorn("ivo://nasa.gsfc.gcn/SWIFT#BAT_GRB_Pos_517234-259")
        self.voevent = v
        self.coords = test_data.arbitrary_eqpos
        self.config =  pysovo.LocalConfig()
    
    def test_formatting_does_not_throw(self):
        observation_text = ami.request_observation(self.coords, 
                                                   "swift_grb", 
                                                   self.voevent,
                                                   self.config)
        
        print
        print "Sample AMI request body text:"
        print observation_text
    
        
