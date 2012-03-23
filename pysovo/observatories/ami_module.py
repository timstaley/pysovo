import pysovo as ps 
import pysovo.email
from astropysics.coords.coordsys import FK5Coordinates 
from observatory import Observatory

import functools

#Try to keep all the variables up front ready for inspection:

ami = Observatory(lat = "+52:12:29",
                  long = "+0:7:21",
                  site_altitude = 15,        
                  tz = 0,
                  target_min_elevation = 20,
                  name = "Arcminute Microkelvin Imager, MRAO",
                  short_name = "AMI",
                  email_address = ps.address_book.ami.email,
                  )

#Attributes specific to this particular site:
ami.default_action = "QUEUE"
ami.default_requester = ps.address_book.ami_requesters['tim']

request_email_subject = "AMI Request"
#Stub function:
ami.check_available = lambda : True #Function that always returns true 

#Request mechanism:
def email_ami(alert_message, 
              local_config, 
              subject=request_email_subject):
    ps.email.send_email(account=local_config.email_account,
                        recipient_addresses=ami.email_address,
                        subject=subject,
                        body_text=alert_message,
                        verbose=True)

ami.internal_request_mechanism = email_ami

##---------------------------------------------------------------
## Implementation from here on in.
def validate_and_typeset_ami_email_alert(array,
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

def format_ami_email_alert(target_coords, target_name, 
                            comment, 
                            action,
                            requester):
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
    
    ra_str = target_coords.ra.getHmsStr(canonical=True).replace(":"," ")
    dec_str = target_coords.dec.getDmsStr(canonical=True).replace(":"," ")
    if target_coords.dec.degrees >= 0:
        dec_str = dec_str[1:]
                                        
    #Also, the comment field has only 256 chars.
    alert_message= validate_and_typeset_ami_email_alert(
                   array = "AMI-LA",
                   target = tgt_str[:16], #slice whole thing just to be sure.,
                   ra = ra_str,
                   dec = dec_str,
                   timing = "ASAP",
                   duration = "01.00",
                   requester = requester,
                   comment = comment[:255],
#                  action = "QUEUE"
                  action = action
                )
    return alert_message


def request_ami_observation(coords, 
                            alert_type, 
                            voevent, 
                            local_config,
                            debug = True,
                            action = None,
                            requester = None):
    ##NB we should re-evaluate these, in case the default is altered after first import.
    if action is None:      
        action = ami.default_action
    if requester is None:
        requester = ami.default_requester
    
    target_name = None
    if alert_type == ps.alert_types.swift_grb:
        target_name = "SWIFT"
        alert_id = voevent.ivorn[len("ivo://nasa.gsfc.gcn/SWIFT#BAT_GRB_Pos_"):]
        comment = "Automated SWIFT ID "+alert_id
    else:
        target_name = "4PISKY"
        comment = "Manual trigger"
      
    alert_message = format_ami_email_alert(coords,
                                            target_name,
                                            comment,
                                            action,
                                            requester)

    ami.internal_request_mechanism(alert_message, local_config)
    return alert_message

ami.request_observation = request_ami_observation
    
