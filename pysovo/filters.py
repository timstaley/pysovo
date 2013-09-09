"""Various bits of logic designed to filter out unwanted VOEvent alerts"""
import voeparse
import pysovo.utils as utils
def reject_swift_bat_trigger(voevent, position):
    """Returns None if all ok, otherwise returns reason for rejection string."""
    params = voeparse.pull_params(voevent)
    dec_limit = 15.0
    if position.dec.degrees < dec_limit:
        return "Target below declination limit of %s degrees" % dec_limit
    st_lost = utils.swift_bool(
                       params["Misc_Flags"]["ImTrig_during_ST_LoL"]['value'])
    if st_lost:
        return "Alert occurred while Swift star-tracker had lost lock."
    grb_identified = utils.swift_bool(
                          params["Solution_Status"]['GRB_Identified']['value'])
    if not grb_identified:
        tgt_in_ground_cat = utils.swift_bool(
                 params["Solution_Status"]['Target_in_Gnd_Catalog']['value'])
        tgt_in_flight_cat = utils.swift_bool(
                 params["Solution_Status"]['Target_in_Flt_Catalog']['value'])
        if tgt_in_ground_cat or tgt_in_flight_cat:
            return "Not a GRB: target associated with known catalog source"
        else:
            return """Not identified as GRB, but not a known source.
                    See packet for further details."""
    return None


