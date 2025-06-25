import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# NOTE: this scope is very important, it is what gives permission to either read/write changes to the calendar
# in this case, i want to use all of google calendar api's so im using ~ auth/calendar ~
# if i would only want to read the user's calendar i would use ~ auth/calendar.readonly ~
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def getCreds():
    creds = None

    if os.path.exists("./sensitive/token.json"):
        creds = Credentials.from_authorized_user_file("./sensitive/token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "./sensitive/credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("./sensitive/token.json", "w") as token:
            token.write(creds.to_json())

    return creds
