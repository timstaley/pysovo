from pysovo import email_alerts


account = email_alerts.load_account_settings_from_file()

test_message= email_alerts.format_ami_alert(
                   array= "AMI-LA",
                   target="Cygnus X-1",
                   ra="19 58 21.676",
                   dec="+35 12 05.78",
                   timing="ASAP",
                   duration="00.30",
                   requester="Staley",
                   comment="Live Test: (ASAP, currently observable) -Cyg X-1 ") 

email_alerts.send_email(account,
                         recipient="someone@somewhere.ac.uk",
                         subject="AMI Request",
                         body_text=test_message,
                         debug=True)

print "Test completed"