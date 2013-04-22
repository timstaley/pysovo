import unittest
import datetime

import pysovo
import pysovo.tests
import pysovo.tests.resources.greenwich as greenwich
from pysovo import contacts
import pysovo.observatories as obs


target_coords = greenwich.circumpolar_north_transit_at_ve_p12hr

obs.ami.request_observation(
                        target_coords,
                        target_name='Test_Target',
                        duration=datetime.timedelta(hours=0.1),
                        timing='ASAP',
                        requested_action='CHECK',
                        requester=contacts['ami']['requester'],
                        recipient_email_address=contacts['test']['email'],
                        email_account=pysovo.default_email_account,
                        comment='FAKE FAKE FAKE - This is just a test.',
                        )


