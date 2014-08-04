"""
Commonly used routines for determining target ephemeris and visibilities.
"""
from __future__ import absolute_import
import ephem
import math
import pytz

DEG_PER_RADIAN = 180 / math.pi


# -----------------------------------------------------------------
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


def get_ephem(eq_posn, observer, current_time):
    """Get basic information on target visibility for a given site.

    Returns a dict populated with relevant TargetStatusKeys.
    """
    keys = TargetStatusKeys
    assert isinstance(observer, ephem.Observer)
    # Get times:

    observer.date = current_time
    fixedbody = ephem.FixedBody()
    fixedbody._ra = eq_posn.ra
    fixedbody._dec = eq_posn.dec
    fixedbody._epoch = eq_posn.epoch
    fixedbody.compute(observer)

    result = {}
    result[keys.site_lst] = str(observer.sidereal_time())
    result[keys.current_pos] = (fixedbody.alt * DEG_PER_RADIAN,
                                fixedbody.az * DEG_PER_RADIAN)
    result[keys.visible_now] = (fixedbody.alt > observer.horizon)

    if fixedbody.neverup:
        result[keys.type] = 'never'
        return result

    result[keys.trans_time] = pytz.utc.localize(
        observer.next_transit(fixedbody).datetime())

    if fixedbody.circumpolar:
        # Circumpolar
        result[keys.type] = 'always'
    else:
        # Regular rise and set
        result[keys.type] = 'sometimes'
        # Returns timezone unaware ('naive') datetimes

        result[keys.rise_time] = pytz.utc.localize(
            observer.next_rising(fixedbody).datetime())
        result[keys.set_time] = pytz.utc.localize(
            observer.next_setting(fixedbody).datetime())

    transit_observer = ephem.Observer()
    transit_observer.lon = observer.lon
    transit_observer.lat = observer.lat
    transit_observer.horizon = observer.horizon
    transit_observer.date = result[keys.trans_time]
    fixedbody.compute(transit_observer)
    result[keys.trans_pos] = (fixedbody.alt * DEG_PER_RADIAN,
                              fixedbody.az * DEG_PER_RADIAN)

    return result
