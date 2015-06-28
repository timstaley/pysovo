import json

import logging
logger = logging.getLogger(__name__)

from pysovo import default_email_config_file
from pysovo import comms

try:
    import contacts
except ImportError as e:
    logger.warning("No contacts module found! "
                "Will import template for unit-testing purposes.")
    import contacts_template as contacts

try:
    default_email_account = comms.email.load_account_settings_from_file(
                                                    default_email_config_file)
    logger.debug("Default email account loaded from %s", default_email_config_file)
except Exception as e:
    logger.warning("Could not load default email account; reason:\n" + e.message)
    default_email_account = None
