import os
from pysovo.tests.resources import __path__ as data_dir
data_dir = data_dir[0]
swift_bat_grb_pos_v2 = os.path.join(data_dir,
                                    'SWIFT_bat_position_v2.0_example.xml')
swift_bat_grb_low_dec = os.path.join(data_dir, 'SWIFT_bat_low_dec.xml')
swift_bat_grb_lost_lock = os.path.join(data_dir, 'BAT_GRB_Pos_558756-820.xml')
swift_bat_known_source = os.path.join(data_dir, 'BAT_GRB_Pos_570069-383.xml')
