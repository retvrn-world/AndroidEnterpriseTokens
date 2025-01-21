from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

import json
from google.auth.transport.requests import Request
from google.auth.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


CLIENT_SECRET_FILE = 'credentials.json'  
SCOPES = ['https://www.googleapis.com/auth/androidmanagement']

service = None

def get_credentials():
    """Gets OAuth 2.0 credentials."""
    creds = None

  
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)


    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            print('flow')
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            print(flow.authorization_url(prompt='consent'))
            print(flow.client_config)
            creds = flow.run_local_server(port=0)
            


        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds

def create_enterprise():
    """Create an enterprise in Android Management API."""
    enterprise = {
        "name": "AndroidShiftEnterprise",  
        "contact_email": "nicholas@retvrn.world",
        "type": "enterprise",
    }
    service = build('androidmanagement', 'v1', credentials=get_credentials())
    result = service.enterprises().create(body=enterprise).execute()
    return result['name']

def generate_enrollment_token(enterprise_name):
    """Generate an enrollment token for the device."""
    service = build('androidmanagement', 'v1', credentials=get_credentials())
    enrollment_token = {
        "name": "My Device",  
    }
    token = service.enterprises().enrollmentTokens().create(parent=f"enterprises/{enterprise_name}", body=enrollment_token).execute()
    return token['url']

if __name__ == "__main__":
    enterprise_name = create_enterprise()
    enrollment_url = generate_enrollment_token(enterprise_name)
    print({'enrollment_url': enrollment_url})
