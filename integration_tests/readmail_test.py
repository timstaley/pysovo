#!/usr/bin/env python
import time
import sys
from pysovo.comms import email
from pysovo.comms.email import keys as acc_keys
from pysovo.local import contacts
import base64
from imbox import Imbox

def make_imbox(account):
    imbox = Imbox('imap.gmail.com',
                  account[acc_keys.username],
                  base64.b64decode(account[acc_keys.password]))
    return imbox

def main():
    account = email.load_account_settings_from_file()

    imbox = make_imbox(account)

    uids = imbox.query_uids(sent_from=account[acc_keys.username],
                                unread=True
                                )
    imbox.logout()
    print "Got ", len(uids), "new test message uids"
#     if len(uids):
#         print "Please read/delete your self-mail before testing! -Exiting"
#         sys.exit(1)

    print "Sending new test-mail..."
    email.send_email(account,
                     recipient_addresses=account[acc_keys.username],
                     subject="[TEST] PYSOVO INTEGRATION TEST",
                     body_text="Ima firin mah lazers!",
                     verbose=True)

    imbox = make_imbox(account)
    msgs = list(imbox.messages(sent_from=account[acc_keys.username],
                                unread=True))
    print "Got ", len(msgs), "new test message uids"
#                                , sent_from='voevent.soton@gmail.com')
    match_uids = imbox.query_uids(sent_from=account[acc_keys.username],
                                unread=True)
    print "Will they remain marked? Got new list of length:", len(match_uids)
    print "Now mark as seen..."
    for uid in match_uids:
        imbox.mark_seen(uid)

    match_uids = imbox.query_uids(sent_from=account[acc_keys.username],
                                unread=True)
    print "Remaining unseen:", len(match_uids)
    
    imbox.logout()

if __name__ == "__main__":
    main()
