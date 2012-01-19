#!/usr/bin/python
import sys, pprint
import angles
from pysovo import voe, voe_utils, email_alerts


email_account = email_alerts.load_account_settings_from_file()

class alert_tags:
    swift_grb="swift_grb"

def main():
    instream = sys.stdin
    s= instream.read()
    v = voe.parseString(s)
    #SWIFT BAT GRB alert:
    if v.ivorn.find("ivo://nasa.gsfc.gcn/SWIFT#BAT_GRB_Pos")==0:
        swift_bat_grb_logic(v)
        
    return 0

def swift_bat_grb_logic(v):
    ww = voe_utils.getWhereWhen(v)
    if float(ww['latitude']) >0.0:
        alert(voevent=v,
              tag = alert_tags.swift_grb,
               ra = ww['longitude'],
               dec = ww['latitude'])

    else:
        notify(voevent=v, 
               tag = alert_tags.swift_grb,
               ra = ww['longitude'], 
               dec = ww['latitude'],
               description="Swift GRB found, but below AMI dec range"
               )


def alert(voevent, tag, ra, dec, description=None):
    """For triggering observations due to high priority events."""
    print "Possible good candidate - alerting now!"
    print "Type:",tag
    print "Ra;dec (decimal):", ra, ";", dec
    
    alert_message = format_swift_ami_grb_alert(voevent.ivorn, ra, dec)
    email_alerts.send_email(email_account,
                         recipient="someone@somewhere.ac.uk",
                         subject="AMI Request",
                         body_text=alert_message,
                         debug=True
                         )
    

def notify(voevent, tag, ra, dec, description=None):
    """For events that are interesting but not worthy of an immediate trigger."""
    print "Noted an interesting VOEvent:"
    print "Type:",tag
    print "Ra;dec (decimal):", ra, ";", dec
    alert_message = "".join(("An unsuitable event was noted.\n"
                             "If suitable, the alert would read as follows:\n"
                             "---------------------------------------------\n",
                             format_swift_ami_grb_alert(voevent.ivorn, ra, dec)
                             ))
    email_alerts.send_email(email_account,
                         recipient="someone@somewhere.ac.uk",
                         subject="AMI Notification",
                         body_text=alert_message,
                         debug=True
                         )
    
    
    
    pass


def format_swift_ami_grb_alert(ivorn, ra, dec):
    swift_ivorn_id=ivorn[len("ivo://nasa.gsfc.gcn/SWIFT#BAT_GRB_Pos_"):]
    ra_sexagesimal=angles.fmt_angle(float(ra))
    dec_sexagesimal=angles.fmt_angle(float(dec))   
    
    test_message= email_alerts.format_ami_alert(
                   array= "AMI-LA",
                   target="SWIFT BAT GRB pos "+swift_ivorn_id,
                   ra=ra_sexagesimal,
                   dec=dec_sexagesimal,
                   timing="ASAP",
                   duration="00.30",
                   requester="Staley",
                   comment="".join(("Automated SWIFT BAT GRB trigger from Soton test system,"
                                    "triggered by ",
                                    ivorn))
                )
    return test_message
        

    
if __name__=='__main__':
    sys.exit(main())
    
