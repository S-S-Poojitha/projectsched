import os
import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pytz
import csv
#handles deletions
SERVICE_ACCOUNTS_DIR = 'service_accounts'
SCOPES = ["https://www.googleapis.com/auth/calendar", "https://www.googleapis.com/auth/calendar.readonly"]

def authenticate(user_email):
    creds = None
    token_path = os.path.join(SERVICE_ACCOUNTS_DIR, f'{user_email}_token.json')

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = Flow.from_client_secrets_file('credentials.json', SCOPES)
            flow.redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'
            auth_url, _ = flow.authorization_url(prompt='consent')
            print('Please go to this URL and authorize access:')
            print(auth_url)

            code = input('Enter the authorization code here:')
            if code:
                flow.fetch_token(code=code)
                creds = flow.credentials
                with open(token_path, 'w') as token:
                    token.write(creds.to_json())

    return creds

def fetch_events(credentials, calendar_id, start_date, end_date):
    service = build('calendar', 'v3', credentials=credentials)
    time_min = start_date.astimezone(pytz.utc).isoformat()
    time_max = end_date.astimezone(pytz.utc).isoformat()
    events_result = service.events().list(calendarId=calendar_id, timeMin=time_min, timeMax=time_max, singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])
    return events

def delete_event(credentials, calendar_id, event_id):
    service = build('calendar', 'v3', credentials=credentials)
    service.events().delete(calendarId=calendar_id, eventId=event_id).execute()

def check_and_delete_events(mail, calendar_id):
    credentials = authenticate(mail)
    IST = pytz.timezone('Asia/Kolkata')
    tomorrow_ist = datetime.date.today() + datetime.timedelta(days=1)
    three_days_later_ist = tomorrow_ist + datetime.timedelta(days=2)
    tomorrow_utc = datetime.datetime.combine(tomorrow_ist, datetime.time.min).astimezone(IST).astimezone(pytz.utc)
    three_days_later_utc = datetime.datetime.combine(three_days_later_ist, datetime.time.max).astimezone(IST).astimezone(pytz.utc)
    events = fetch_events(credentials, calendar_id, tomorrow_utc, three_days_later_utc)
    for event in events:
        event_id = event['id']
        attendees = event.get('attendees', [])
        if any(attendee.get('responseStatus') == 'declined' for attendee in attendees):
            delete_event(credentials, calendar_id, event_id)
            print(f"Deleted event with ID: {event_id}")
            output_file = 'declined_attendees.csv'  # Specify the output CSV file
            with open(output_file, 'a', newline='') as csvfile:
                fieldnames = ['Event ID', 'Attendee Email']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                for attendee in attendees:
                    if attendee.get('responseStatus') == 'declined':
                        writer.writerow({'Event ID': event_id, 'Attendee Email': attendee.get('email')})
# Example usage
if __name__ == "__main__":
    calendar_id = 'REPLACE_WITH_YOUR_MAIL_ID'  # Replace with your calendar ID
    check_and_delete_events(calendar_id, calendar_id)
