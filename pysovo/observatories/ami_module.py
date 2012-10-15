#pysovo VOEvent Tools
#Interface to AMI observatory
#Copyright Tim Staley, <timstaley337@gmail.com>, 2012

import pysovo as ps
import pysovo.email
from astropysics.coords.coordsys import FK5Coordinates
from observatory import Observatory

import functools
import datetime

#Try to keep all the variables up front ready for inspection:

ami = Observatory(lat='+52:12:29',
                  long='+0:7:21',
                  site_altitude=15,
                  tz=0,
                  target_min_elevation=20,
                  name='Arcminute Microkelvin Imager, MRAO',
                  short_name='AMI',
                  email_address=ps.address_book.ami.email,
                  )

#Attributes specific to this particular site:
ami.default_action = 'QUEUE'
ami.default_requester = ps.address_book.ami_requesters['tim']

request_email_subject = 'AMI Request'
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

#Formatting specification, for reference:
"""
  Array=     AMI-SA
  Target=    GRB110328A
  J2000RA=   16 44 49.93
  J2000Dec=  57 35 59.1
  Timing=    ST 15.45
  Duration=  02.00
  Requester= djt
  Comment=   Target of Opportunity test

where:

 'Array'     must be either 'AMI-SA' or 'AMI-LA'.
 'Target' and the J2000 coordinates define the observation target.
 'Timing'    specifies the start of the observation, either by Local
             Sidereal Time 'ST hh.mm', or by using one of the keywords
             'Transit' (to observe through transit) or 'ASAP' (to start
             the observation as soon as possible).
 'Duration'  specifies the length of the observation (hh.mm).
 'Requester' identifies the observer.
 'Comment'   adds a string of comment text to the observation header.
"""


def format_ami_coords(coords):
    """Converts astropysics FK5 coords to AMI formatted ra,dec strings."""

    ra_str = coords.ra.getHmsStr(canonical=True).replace(':', ' ')
    dec_str = coords.dec.getDmsStr(canonical=True).replace(':', ' ')
    if coords.dec.degrees >= 0:
        dec_str = dec_str[1:]
    return ra_str, dec_str

def format_ami_duration(duration):
    """Format duration string in AMI compliant format.
    
    Rounds down to nearest minute.
    """
    assert isinstance(duration, datetime.timedelta)
    hrs = duration.seconds // 3600
    minutes = (duration.seconds - hrs * 3600) // 60
    return '.'.join((str(hrs).zfill(2), str(minutes).zfill(2)))

def validate_and_typeset_ami_email_alert(
                    target_coords,
                    target_name,
                    timing,
                    action,
                    requester,
                    duration,
                    comment='',
                    array='AMI-LA'
                    ):
    """
    Validates the tightly constrained fields, and enforces formatting.
    
    *Args*
    - target_coords: Should be astropysics.coordinates.coordsys.FK5Coordinates
    
    - target_name: String, up to 16 chars (any overrun will be dropped)
    
    - timing: String specifying when to observe, one of  ['ASAP', 'Transit', 'ST'] 
        i.e.:  -as soon as possible, when transiting, or at a specified
        sidereal time (last option not currently supported).    
        
    - action:  Either 'QUEUE' (queue the request) or any of 3 synonyms,
            ['CHECK', 'VERIFY', 'QUERY'], which will result in a reply email
            detailing request validity and observing conditions,
            but will not actually queue the observation.
            
    - requester: The requester's identity.
    
    - duration: datetime.timedelta - requested observation length 
        (sensibly this should be anywhere from 30 minutes to a few hours).
    
    - comment: String, up to 256 chars (any overrun will be dropped)
    
    - Array: String, One of ['AMI-LA', 'AMI-SA'].
    
    *Returns*:
    String, formatted email body. 
    """

    if array not in ['AMI-LA', 'AMI-SA']:
        raise ValueError('Invalid AMI array choice')

    if timing not in ['ASAP', 'Transit']:
        if timing.find('ST') != 0:
            raise ValueError('Invalid AMI timing choice')

    if action not in ['QUERY', 'CHECK', 'VERIFY', 'QUEUE']:
        raise ValueError('Invalid AMI action choice')

    assert isinstance(target_coords, FK5Coordinates)

    ra_str, dec_str = format_ami_coords(target_coords)
    duration_str = format_ami_duration(duration)

    #Ami target field has only 16 chars.
    #Also, the comment field has only 256 chars.
    alert_text = ''.join([  'Array=     ', array, '\n',
                            'Target=    ', target_name[:16], '\n',
                            'J2000RA=   ', ra_str, '\n',
                            'J2000Dec=  ', dec_str, '\n',
                            'Timing=    ', timing, '\n',
                            'Duration=  ', duration_str, '\n',
                            'Requester= ', requester, '\n',
                            'Comment=  ', comment[:255], '\n',
                            'Action=  ', action, '\n',
                            ])
    return alert_text

def request_ami_observation(coords,
                            alert_type,
                            voevent,
                            local_config,
                            duration=datetime.timedelta(hours=1.0),
                            debug=True,
                            action=None,
                            requester=None):
    """Generates an appropriate AMI observation request."""

    if action is None:
        action = ami.default_action
    if requester is None:
        requester = ami.default_requester

    target_name = None
    if alert_type == ps.alert_types.swift_grb:
        alert_id = voevent.attrib['ivorn'][len('ivo://nasa.gsfc.gcn/SWIFT#BAT_GRB_Pos_'):]
        alert_id_short = alert_id.split('-')[0]
        target_name = 'SWIFT_' + alert_id_short
        comment = 'Automated SWIFT ID ' + alert_id
    else:
        target_name = '4_PI_SKY'
        comment = 'Manual trigger'

    alert_message = validate_and_typeset_ami_email_alert(target_coords=coords,
                                                 target_name=target_name,
                                                 timing='ASAP',
                                                 action=action,
                                                 requester=requester,
                                                 duration=duration,
                                                 comment=comment)

    ami.internal_request_mechanism(alert_message, local_config)
    return alert_message

ami.request_observation = request_ami_observation

