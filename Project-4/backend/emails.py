from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError
from email.mime.text import MIMEText
import base64
from googleapiclient.discovery import build
import secrets

def sendEmail(email):
    # Scopes for Gmail API access
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']

    # Get credentials via OAuth 2.0 flow
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    credentials = flow.run_local_server(port=0)

    # Save and load credentials for later use
    creds = credentials.to_json()
    with open('token.json', 'w') as token:
        token.write(creds)

    # Build Gmail service with obtained credentials
    service = build('gmail', 'v1', credentials=credentials)

    # Creating the link being sent:
    token = secrets.token_hex(10)
    link = "https://romanempire.online/verify/"+token

    email_token_collection.insert_one({"email":email,"token":token})

    # Should change sender@gmail.com
    message = create_message('sender@gmail.com', email, 'Trajan Marketplace Email Confirmation', 'Click the link below to verify account\n'+link)
    send_message(service, 'me', message)

def create_message(sender, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    return {'raw': raw_message}

# Function to send a message
def send_message(service, user_id, message):
    try:
        message = service.users().messages().send(userId=user_id, body=message).execute()
        print('Message Id: %s' % message['id'])
        return message
    except HttpError as error:
        print('An error occurred: %s' % error)
