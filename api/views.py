from __future__ import print_function

from django.shortcuts import render

import json

import datetime
import os.path
from pathlib import Path
from django.shortcuts import redirect, render
BASE_DIR = Path(__file__).resolve().parent.parent

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Create your views here.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def GoogleCalendarInitView(request):
    # start google oauth here
    creds = None
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            with open(os.path.join(BASE_DIR, 'credentials.json')) as secrets_file:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
    request.session['creds'] = creds.to_json()
    return redirect('GoogleCalendarRedirectView')
    

def GoogleCalendarRedirectView(request):
    json_loaded = json.loads(request.session['creds'])
    creds = Credentials(
        json_loaded['token'],
        refresh_token=json_loaded['refresh_token'],
        token_uri=json_loaded['token_uri'],
        client_id=json_loaded['client_id'],
        client_secret=json_loaded['client_secret'],)
    service = build('calendar', 'v3', credentials=creds)
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    if not events:
        events.append('No events upcoming')
    return render(request, "events_list.html", {'events':events})
