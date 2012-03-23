import pysovo as ps
import datetime, pytz
from pysovo import email, sms

#TODO: Decoupling of simple string formatting and on-sky / off-sky case determination.

#----------------------------------------------------
#Settings:
signoff_long = "4 Pi Sky Bot"
signoff_short = "4PiSkyBot"

datetime_format_long = "%y-%m-%d %H:%M:%S (%A)"
datetime_format_short = "%a%H:%M"
time_format_short = "%H:%M"
#----------------------------------------------------
def notify(local_config,
           recipients, 
           subject,
           long_message,
           send_sms = False,
           short_message = None,
           ):
    """
    Takes a list of recipients and sends them messages via multiple mechanisms where applicable.
    
    Recipients should be class / tuple with .email and .mobile attributes.
    (see pysovo.address_book)
    """
    recipients = ps.utils.listify(recipients)
        
    email.send_email(local_config.email_account,
                         recipient_addresses=[ r.email for r in recipients],
                         subject=subject,
                         body_text = long_message,
                         verbose = True)
    
    if send_sms and (short_message is not None) and (local_config.sms_account is not None):
        sms_recipients = [r.mobile for r in recipients if r.mobile is not None]
        
        sms.send_sms(local_config.sms_account,
                             sms_recipients,
                             short_message,
                             debug=True)
        
#-----------------------------------------------------------------------------------        
def noted_message(eq_posn,
                  event_time,
                  description,):
    long_msg = """At {tm} a {desc} was noted at:\n{posn}""".format(
                    tm=event_time.strftime(datetime_format_long), 
                    desc=description,
                    posn = eq_posn)

    
    if len(description)>20:
        short_desc = description[:20]+"...'"
    else:
        short_desc = description
    
    short_msg ="""{desc} noted at {tm}""".format(
                 tm=event_time.strftime(datetime_format_short),
                 desc="'"+short_desc+"'")
    return long_msg, short_msg

def signoff_message():
    long_sign = """Regards,\n{sign}.""".format(sign=signoff_long)
    short_sign = '-'+signoff_short
    return long_sign, short_sign

def event_missed_message( eq_posn,
                          event_time,
                          description,
                          reason_missed
                         ):
    long_note, short_note = noted_message(eq_posn, event_time, description)
    
    long_miss = """Unfortunately, the event will not be followed up """
    long_miss+= """due to the following reason:\n{reason}""".format(reason=reason_missed)
    
    short_miss = """ but not observed: {reason}.""".format(reason=reason_missed[:40])
    
    long_sign, short_sign = signoff_message()
    
    long_msg = "\n\n".join((long_note, long_miss, long_sign))
    short_msg = "".join((short_note, short_miss, short_sign))
    
    return long_msg, short_msg[:159]

    

def format_target_status_text(eq_posn, obs_site, current_time):
    assert isinstance(obs_site, ps.observatories.observatory.Observatory)
    rise, set, transit = obs_site.next_riseSetTransit(eq_posn, current_time,
                                                      alt = obs_site.target_min_elevation)
    
    if transit is None:
        return ("Bad request: Target not visible from this observatory around this date.",
                 "Target not visible") #(long_msg, short_msg)
    
    transit_pos = obs_site.apparentCoordinates(eq_posn, transit)
    
    long_status=""
    short_status="Status:"
    
    target_is_on_sky = obs_site.on_sky(eq_posn, current_time)
    
    if (not target_is_on_sky) and (rise is not None): #Shouldn't need the second test, (not on sky-> not circumpolar -> rise!=None) but check anyway in case of user error.
        long_status += "The target is off sky and will rise next at {rise}\n\n".format(rise=rise.strftime(datetime_format_long))
        short_status +=  """Off sky, rise@{rise}.""".format(rise=rise.strftime(datetime_format_short))   
    elif target_is_on_sky:
        sky_position = obs_site.apparentCoordinates(eq_posn, current_time)
        long_status +=  """The target is on sky currently, at position:\n{pos}\n\n""".format(pos = sky_position[0]) 
        short_status += """ON SKY!"""
    
    long_status += """The target transits at {trans_time} around the position:\n{transit_pos}\n""".format(
              trans_time = transit.strftime(datetime_format_long), transit_pos = transit_pos[0] )

    if set is not None:
        long_status += """and sets at {set}.""".format(set=set.strftime(datetime_format_long) )
    else: #set=None --> Always visible
        long_status += """and is always visible (circumpolar)."""
    return long_status, short_status


def obs_requested_message(eq_posn,
                          event_time,
                          description,
                          obs_site,
                          current_time
                           ):
    
    note_long, note_short = noted_message(eq_posn, event_time, description)
    
    tgt_status_long, tgt_status_short = format_target_status_text( eq_posn, 
                                                                  obs_site, 
                                                                  current_time
                                                                   )

    request_long = """\
An observation has been requested from : {obs_nm_short}, ({obsname})
The local sidereal time at {obs_nm_short} is {obs_lst}.""".format(
              obs_nm_short = obs_site.short_name,
               obsname = obs_site.name,
               obs_lst = obs_site.localSiderialTime(current_time, returntype='string'),
               )

    
    request_short ="""obs@{site}""".format(site=obs_site.short_name)
    
    sign_long, sign_short = signoff_message()
    
    long_msg = "\n\n".join((note_long, tgt_status_long, request_long ,sign_long))
    short_msg = " ".join((note_short, tgt_status_short, request_short, sign_short))
    return long_msg, short_msg[:155]


        
    
    
