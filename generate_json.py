import os

def generate_json():
    my_json = {}
    my_json["type"] = os.environ.get('CRED_TYPE')
    my_json["project_id"] = os.environ.get('CRED_PROJECT_ID') 
    my_json["private_key_id"] = os.environ.get('CRED_PRIVATE_KEY_ID')
    my_json["private_key"] = os.environ.get('CRED_PRIVATE_KEY')
    my_json["client_email"] = os.environ.get('CRED_CLIENT_EMAIL')
    my_json["client_id"] = os.environ.get('CRED_CLIENT_ID')
    my_json["auth_uri"] = os.environ.get('CRED_AUTH_URI')
    my_json["token_uri"] = os.environ.get('CRED_TOKEN_URI')
    my_json["auth_provider_x509_cert_url"] = os.environ.get('CRED_AUTH_PROVIDER_X509_CERT_URL')
    my_json["client_x509_cert_url"] = os.environ.get('CRED_CLIENT_X509_CERT_URL')
    return my_json
