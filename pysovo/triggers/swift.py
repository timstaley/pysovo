"""
Convenience routines and data structures useful for dealing with Swift packets.
"""

import voeparse
from pysovo.utils import convert_voe_coords_to_fk5


def swift_bool(bstring):
        if bstring == 'true':
            return True
        elif bstring == 'false':
            return False
        else:
            raise ValueError("This string does not appear to be a SWIFT VOEvent "
                              "boolean: %s" % bstring)

class filters:
    @staticmethod
    def is_bat_grb_pkt(voevent):
        ivorn = voevent.attrib['ivorn']
        if ivorn.find("ivo://nasa.gsfc.gcn/SWIFT#BAT_GRB_Pos") == 0:
            return True
        return False

    @staticmethod
    def startracker_lost(params):
        return swift_bool(
                       params["Misc_Flags"]["ImTrig_during_ST_LoL"]['value'])

    @staticmethod
    def grb_identified(params):
        return swift_bool(
                      params["Solution_Status"]['GRB_Identified']['value'])

    @staticmethod 
    def tgt_in_ground_cat(params):
        return swift_bool(
             params["Solution_Status"]['Target_in_Gnd_Catalog']['value'])

    @staticmethod 
    def tgt_in_flight_cat(params):
        return swift_bool(
             params["Solution_Status"]['Target_in_Flt_Catalog']['value'])


class BatGrb:
    def __init__(self, voevent):
        self.voevent = voevent
        if not filters.is_bat_grb_pkt(voevent):
            raise ValueError("Cannot instantiate BatGrb; packet header mismatch.")

        self.description = "Swift BAT GRB - initial position"
        id_long_short = BatGrb._pull_swift_bat_id(self.voevent)
        self.id_long = 'SWIFT' + id_long_short[0]
        self.id = 'SWIFT_' + id_long_short[1]
        #Assigned name according to the 'why' section of voevent packet:
        self.inferred_name = self.voevent.Why.Inference.Name
        self.isotime = voeparse.pull_isotime(self.voevent)
        self.params = voeparse.pull_params(self.voevent)
        self.position = convert_voe_coords_to_fk5(
                                       voeparse.pull_astro_coords(self.voevent))

    def reject(self):
        """
        Returns None if all ok, otherwise returns 'reason for rejection' string.
        """
        pars = self.params
        if filters.startracker_lost(pars):
            return "Alert occurred while Swift star-tracker had lost lock."

        # if not filters.grb_identified(pars):
        #     if filters.tgt_in_ground_cat(pars) or filters.tgt_in_flight_cat(pars):
        #         return "Not a GRB - target associated with known catalog source"
        #     else:
        #         return """Not identified as GRB, but not a known source.
        #                 See packet for further details."""
        return None

    @staticmethod
    def _pull_swift_bat_id(voevent):
        alert_id = voevent.attrib['ivorn'][len('ivo://nasa.gsfc.gcn/SWIFT#BAT_GRB_Pos_'):]
        alert_id_short = alert_id.split('-')[0]
        return alert_id, alert_id_short

