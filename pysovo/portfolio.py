#pysovo VOEvent Tools
#Tim Staley, <timstaley337@gmail.com>, 2012
#

#Work on hold for now...

#from VOEventLib import VOEvent as voe, Vutil as voe_utils
#import utils
#
#class Portfolio(object):
#    def __init__(self, 
#                 init_ivorn,
#                 skyalert_id=None,
#                 init_isotime=None,
#                 skyalert_timestamp=None
#                 ):
#        self.init_ivorn=init_ivorn
#        self.init_isotime=init_isotime
#        self.skyalert_id=skyalert_id
#        self.skyalert_timestamp=skyalert_timestamp
#        self.voevents={} #maps ivorn --> voe.VOEvent
#        self.params_best={}
#        self.params_hist={}
#
#    @classmethod
#    def from_init_ivorn(init_ivorn):
#        return Portfolio(init_ivorn)
#        
#    @classmethod
#    def from_init_voevent(v):
#        """v is a voe.VOEvent"""
##        assert isinstance(v, voe.VOEvent)
#        t = utils.get_isotime(v)
#        pf = Portfolio(v.ivorn, init_isotime=t)
#        return pf
#        
#    @classmethod
#    def from_skyalert_portfolio(skyalert_pf_dict, 
#                                init_ivorn, 
#                                skyalert_event_id,
#                                skyalert_time):
#        """Portfolio dictionary should be a mapping,
#         ivorn->Voevent."""
#        pf = Portfolio(init_ivorn,
#                        skyalert_id = skyalert_event_id,
#                        init_isotime = None,
#                        skyalert_timestamp = skyalert_time)
#        pf.voevents = Portfolio._convert_skyalert_pf_dict_to_voe(skyalert_pf_dict)
#        pf.init_isotime = utils.get_isotime(
#                                       pf.voevents[init_ivorn])
#        return pf
#    
#    @classmethod
#    def _convert_skyalert_pf_dict_to_voe(skyalert_pf_dict):
#        pass
#    
