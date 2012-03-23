import pysovo as ps
import pysovo.observatories as obs
from astropysics.coords.coordsys import FK5Coordinates 
import datetime, pytz
def main():
    local_config = ps.LocalConfig(email_account = ps.email.load_account_settings_from_file(),
                              sms_account = ps.sms.load_account_settings_from_file())
    
    target_coords = FK5Coordinates(("23:15:00 +35.000 J2000.0"))
    ra = target_coords.ra.getHmsStr(canonical=True).replace(":"," "),
    dec = target_coords.dec.getDmsStr(canonical=True).replace(":"," ")
    
    print "RA,DEC:", ra, dec
    
    def dummy_func(request_info, local_config):
        print "Request email:"
        print "-------------------------------"
        print request_info
        print "-------------------------------"
        pass
    obs.ami.internal_request_mechanism = dummy_func
    obs.ami.default_action="QUERY"
    
    msg = obs.ami.request_observation(target_coords, alert_type="test", 
                                voevent=None,
                                local_config=local_config)
#    dummy_func(msg, local_config=None)
    
    now = datetime.datetime.now(pytz.utc)
    long_msg, short_msg = ps.notifications.obs_requested_message(target_coords, 
                                      event_time=now, #should grab from voevent
                                      description="Manual trigger",
                                      obs_site = obs.ami,
                                      current_time=now)
    
    print long_msg
#    ps.notifications.notify(local_config,
#                             ps.address_book.test, 
#                             "[TEST] Fermi target status ", 
#                             long_msg, 
#                             send_sms=False)
    pass


if __name__ == "__main__":
    main() 
