import datetime, pytz
import astropysics.obstools

import jinja2
from jinja2 import Environment, PackageLoader
env = Environment(loader=PackageLoader('pysovo', 'templates'),
                  trim_blocks=True)
#----------------------------------------------------
datetime_format_long = "%y-%m-%d %H:%M:%S (%A)"
datetime_format_short = "%a%H:%M"
time_format_short = "%H:%M"
def format_datetime(dt, format=None):
    if format:
        return dt.strftime(format)
    else:
        return dt #Converts to a reasonable default string anyway.

env.filters['datetime'] = format_datetime
#------------------------------------------------------------------------------
long_template = env.get_template('notify_long.txt')

def generate_report_text(target_info, sites, dtime, actions_taken):
    posn = target_info['position']
    site_reports = [(site, site_report(posn, site, dtime))
                            for site in sites]
    return long_template.render(target=target_info,
                                note_time=dtime,
                                site_reports=site_reports,
                                actions_taken=actions_taken,
                                dt_style=datetime_format_long)

#-----------------------------------------------------------------
## Context creation routines:

class TargetStatusKeys():
    """A namespaced set of dict keys for site report contexts"""
    site_lst = 'site_lst'
    type = 'type'
    visible_now = 'visible_now'
    current_pos = 'current_position'
    trans_time = 'transit_time'
    trans_pos = 'transit_position'
    rise_time = 'rise_time'
    set_time = 'set_time'

def site_report(eq_posn, obs_site, current_time):
    """Returns a dict populated with relevant TargetStatusKeys."""
    keys = TargetStatusKeys
    assert isinstance(obs_site, astropysics.obstools.Site)
    #Get times:
    rise, set, transit = obs_site.nextRiseSetTransit(eq_posn, current_time,
                                              alt=obs_site.target_min_elevation)
    result = {}
    result[keys.site_lst] = obs_site.localSiderialTime(current_time,
                                                       returntype='string')
    if transit is None:
        #Wrong hemisphere
        result[keys.type] = 'never'
        return result

    if set is None:
        #Circumpolar
        result[keys.type] = 'always'
    else:
        #Regular rise and set
        result[keys.type] = 'sometimes'
        result[keys.rise_time] = rise
        result[keys.set_time] = set

    result[keys.trans_time] = transit
    result[keys.trans_pos] = obs_site.apparentCoordinates(eq_posn, transit)[0]
    result[keys.visible_now] = obs_site.onSky(eq_posn, current_time,
                                      alt=obs_site.target_min_elevation)

    if result[keys.visible_now]:
        ac_list = obs_site.apparentCoordinates(eq_posn, current_time)
        result[keys.current_pos] = ac_list[0]
    return result
