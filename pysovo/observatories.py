import astropysics.obstools
from astropysics.coords.coordsys import FK5Coordinates 

import email_alerts
import private_details

# Based on
# http://packages.python.org/Astropysics/coremods/obstools.html#astropysics.obstools.Site
# NB abstract base class, just suggests a standard interface.
class Observatory(astropysics.obstools.Site):
    """Extends astropysics.obstools.site - Adds various simple attributes. """
    def __init__(self, lat, long, alt=0, tz=None, name=None):
        astropysics.obstools.Site.__init__(self, lat, long, alt, tz, name)
        self.email_address = None
        self.ip_address = None 
        
    @staticmethod
    def send_alert(coords, **kwargs):
        """ This should be implemented and assigned on a per-observatory basis. 
            (No point trying to choose a common parameter set at this stage, if ever).
        """
        raise NotImplementedError
    

#---------------------------------------------------------------------------------------
#AMI
ami = Observatory(lat = "+52:12:29",
                  long = "+0:7:21",
                  alt = 15,         
                  name = "Arcminute Microkelvin Imager, MRAO")
#ami.lon, ami.lat = "+0:7:21", "+52:12:29"
#ami.elevation = 15
ami.email_address = private_details.email_addresses["ami"]


def _typeset_ami_email_alert(array,
                    target,
                    ra,
                    dec,
                    timing,
                    duration,
                    requester,
                    comment,
                    action):

    if array not in ["AMI-LA", "AMI-SA"]:
        raise ValueError("Invalid AMI array choice")
    
    if timing not in ["ASAP", "Transit"]:
        if timing.find("ST")!=0:
            raise ValueError("Invalid AMI timing choice")
    
    if action not in ["QUERY", "CHECK", "VERIFY", "QUEUE"]:
        raise ValueError("Invalid AMI action choice")
    
    
    alert_text = "".join(["Array=     ",array,"\n",
                "Target=    ", target, "\n"
                "J2000RA=   ", ra,"\n",
                "J2000Dec=  ", dec, "\n",
                "Timing=    ", timing, "\n",
                "Duration=  ", duration, "\n",
                "Requester= ", requester, "\n",
                "Comment=  ", comment, "\n"
                "Action=  ", action, "\n"
                ])
    return alert_text

def _format_ami_email_alert(target_coords, target_name, comment):
    assert isinstance(target_coords, FK5Coordinates)
     
    if target_coords.dec.degrees > 0:
        dec_sign = "P"
    else:
        dec_sign = "M"
        
    #Ami target field has only 16 chars.
    #we use 5 for formatting, 3 for RA, 2 for Dec = 6 left over
    tgt_str = "{t}_R{r}_D{s}{d}".format(t = target_name[:6], 
                                        r = int(target_coords.ra.degrees), 
                                        s = dec_sign, 
                                        d = abs(int(target_coords.dec.degrees))
                                        )
                                        
    #Also, the comment field has only 256 chars.
    alert_message= _typeset_ami_email_alert(
                   array = "AMI-LA",
                   target = tgt_str[:16], #slice whole thing just to be sure.,
                   ra = target_coords.ra.getHmsStr(canonical=True).replace(":"," "),
                   dec = target_coords.dec.getDmsStr(canonical=True).replace(":"," "),
                   timing = "ASAP",
                   duration = "01.00",
                   requester = private_details.ami_requesters["me"],
                   comment = comment[:255],
                  action = "QUEUE"
                )
    return alert_message




def _send_ami_alert(coords, alert_type, alert_id, 
                    email_account=None,
                    debug = True):
    if email_account==None:
        email_account=email_alerts.load_account_settings_from_file()
    
    target_name=None
    if alert_type=="swift_grb":
        target_name = "SWIFT"
        comment = "Automated SWIFT ID "+alert_id
    
    alert_message = _format_ami_email_alert(coords, 
                                            target_name, 
                                            comment)
    if debug:
        print "Sending message:"
        print alert_message
        
    email_alerts.send_email(email_account,
                         recipient = ami.email_address,
                         subject = "AMI Request",
                         body_text = alert_message,
                         debug = debug
                         )

ami.send_alert = _send_ami_alert #Python joy!
    
#END AMI    
#---------------------------------------------------------------------------------------    
