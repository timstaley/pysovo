from __future__ import absolute_import
import sys
import os
import logging
logger = logging.getLogger(__name__)

config_folder = os.path.join(os.environ['HOME'], '.pysovo')
contacts_file = os.path.join(config_folder, 'contacts.json')
default_email_config_file = os.path.join(config_folder, "email_acc")

import pysovo.comms
import pysovo.ephem
import pysovo.utils

