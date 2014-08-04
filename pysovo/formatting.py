"""Various code snippets used for formatting messages"""
from __future__ import absolute_import
from pysovo.visibility import DEG_PER_RADIAN
#----------------------------------------------------
datetime_format_long = "%Y-%m-%d %H:%M:%S (%A)"
datetime_format_short = '%y%m%d-%H%M.%S'
day_time_format_short = "%a%H:%M"
time_format_short = "%H:%M"
#----------------------------------------------------
def format_datetime(dt, format=None):
    if format:
        return dt.strftime(format)
    else:
        return dt #Converts to a reasonable default string anyway.

def rad_to_deg(rad):
    return rad*DEG_PER_RADIAN
