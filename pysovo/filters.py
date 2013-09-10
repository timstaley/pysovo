"""Various bits of logic designed to filter out unwanted VOEvent alerts"""
import voeparse
import pysovo.utils as utils

class ami:
    @staticmethod
    def reject(position):
        dec_limit = 15.0
        if position.dec.degrees < dec_limit:
            return "Target below declination limit of %s degrees" % dec_limit
        return None


