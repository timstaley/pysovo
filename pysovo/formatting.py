"""Various code snippets used for formatting messages"""
#----------------------------------------------------
datetime_format_long = "%y-%m-%d %H:%M:%S (%A)"
datetime_format_short = '%y%m%d-%H%M.%S'
day_time_format_short = "%a%H:%M"
time_format_short = "%H:%M"
#----------------------------------------------------
def format_datetime(dt, format=None):
    if format:
        return dt.strftime(format)
    else:
        return dt #Converts to a reasonable default string anyway.
