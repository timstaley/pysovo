def generate_autocomplete_dictionary_keys(dummy_key_class):
    for att_name, att_val in vars(dummy_key_class).iteritems():
        if(att_name[:2]!="__" and att_val==None):
            setattr(dummy_key_class, att_name, "".join([dummy_key_class.__name__,"_",att_name]))
            
            
class email_account:
    username=None
    smtp_server=None
    smtp_port=None
    password=None
    
generate_autocomplete_dictionary_keys(email_account)