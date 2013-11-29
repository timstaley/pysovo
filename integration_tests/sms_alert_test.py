#!/usr/bin/env python
import pysovo as ps
import pysovo.sms as sms

def main():
    acc = sms.load_account_settings_from_file()
    sms_balance = sms.check_sms_balance(acc)
    print "SMS Balance:", sms_balance
    print "(", sms_balance/0.8 , " UK texts )"
    
    #msg_ids = sms.send_sms(acc, "447751000000", "Hello world", debug=True)
    #msg_ids = sms.send_sms(acc, ps.address_book.tim.mobile, "Hello world", debug=True)
    #
    #print "Delivery statuses:"
    #print sms.check_sms_statuses(acc, msg_ids)

if __name__ == "__main__":
    main() 




