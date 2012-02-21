#!/usr/bin/python

import pysovo.sms_alerts as sms

acc = sms.load_account_settings_from_file()

print "SMS Balance:", sms.check_sms_balance(acc)

msg_ids = sms.send_sms(acc, "001122334455", "Hello world", debug=True)

print "Delivery statuses:"
print sms.check_sms_statuses(acc, msg_ids)





