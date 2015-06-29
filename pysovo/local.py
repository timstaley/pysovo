import logging
logger = logging.getLogger(__name__)

## Check for a private contacts module:
try:
    import contacts
except ImportError as e:
    logger.warning("No contacts module found! "
                "Will import template for unit-testing purposes.")
    import contacts_template as contacts