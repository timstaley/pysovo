"""
Commonly used routines for determining target ephemeris and visibilities.
"""

import datetime, pytz
import astropysics.obstools

#-----------------------------------------------------------------
class TargetStatusKeys():
    """A namespaced set of dict keys for visibility reports"""
    site_lst = 'site_lst'
    type = 'type'
    visible_now = 'visible_now'
    current_pos = 'current_position'
    trans_time = 'transit_time'
    trans_pos = 'transit_position'
    rise_time = 'rise_time'
    set_time = 'set_time'

def visibility(eq_posn, obs_site, current_time):
    """Get basic information on target visibility for a given site.

    Returns a dict populated with relevant TargetStatusKeys.
    """
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
