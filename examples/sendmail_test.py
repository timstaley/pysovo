from pysovo import email_alerts, private_details


account = email_alerts.load_account_settings_from_file()

test_message= """
Hello, world!
I'm a python email script. 
"""

email_alerts.send_email(account,
                         recipient=private_details.email_addresses["test"],
                         subject="Python email test",
                         body_text=test_message,
                         debug=True)

print "Test completed"