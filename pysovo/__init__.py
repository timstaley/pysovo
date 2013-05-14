from __future__ import absolute_import
import os
import json
import logging
import sys
logger = logging.getLogger(__name__)

config_folder = os.path.join(os.environ['HOME'], '.pysovo')
default_email_config_file = os.path.join(config_folder, "email_acc")

import pysovo.comms
import pysovo.utils
import pysovo.notify

try:
    contacts_file = os.path.join(config_folder, 'contacts.json')
    with open(contacts_file) as f:
        contacts = json.load(f)
    logger.debug('Contacts loaded from ' + contacts_file)
except Exception as e:
    logger.warn("Could not load contacts file; reason:\n" + str(e))
    contacts = {}

try:
    default_email_account = comms.email.load_account_settings_from_file(
                                                    default_email_config_file)
    logger.debug("Default email account loaded from %s", default_email_config_file)
except Exception as e:
    logger.warn("Could not load default email account; reason:\n", +str(e))
    default_email_account = None







