from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from datetime import *
import dateutil.parser as dparser
from tzlocal import get_localzone


try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    SCOPES = 'https://www.googleapis.com/auth/calendar'
    CLIENT_SECRET_FILE = 'client_secret.json'
    APPLICATION_NAME = 'Google Calendar API Python Quickstart'

    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    
    return credentials

def create_event(event_dict):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    cal = discovery.build('calendar', 'v3', http=http)

    DEFAULT = datetime.now().replace(second=0, minute=0, microsecond=0) + timedelta(hours=1)
    local_tz = get_localzone()

    #event_dict = combined.get_event_dict(filename)
    #print(event_dict)

    summary = event_dict['name']
    location = event_dict['location']
    try:
        startDateTime = local_tz.localize(dparser.parse(event_dict['start_date'] + ' ' + event_dict['start_time'],
                                fuzzy=True, default=DEFAULT))
    except ValueError:
        startDateTime = local_tz.localize(dparser.parse(str(DEFAULT)))
    startDateTime_str = startDateTime.strftime("%Y-%m-%dT%H:%M:%S%z")
    
    try:
        endDateTime = local_tz.localize(dparser.parse(event_dict['end_date'] + ' ' + event_dict['end_time'],
                                fuzzy=True, default=DEFAULT))
        if event_dict['end_time'] == '':
            endDateTime = startDateTime + timedelta(hours=1)
    except ValueError:
        endDateTime = startDateTime + timedelta(hours=1)
    endDateTime_str = endDateTime.strftime("%Y-%m-%dT%H:%M:%S%z")

    event = {'summary': summary,
             'location': location,
             'start': {'dateTime': startDateTime_str},
             'end': {'dateTime': endDateTime_str}
             }
    event = cal.events().insert(calendarId='primary', body=event).execute()

