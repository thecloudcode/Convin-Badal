from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from django.conf import settings
from rest_framework import views
from rest_framework.response import Response

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

class GoogleCalendarInitView(views.APIView):
    def get(self, request):
        flow = InstalledAppFlow.from_client_secrets_file(settings.CLIENT_SECRET_FILE, SCOPES)
        authorization_url, state = flow.authorization_url(prompt='consent')

        return Response({'authorization_url': authorization_url, 'state': state})

class GoogleCalendarRedirectView(views.APIView):
    def get(self, request):
        code = request.GET.get('code')
        state = request.GET.get('state')

        flow = InstalledAppFlow.from_client_secrets_file(settings.CLIENT_SECRET_FILE, SCOPES, state=state)
        flow.fetch_token(code=code)
        credentials = flow.credentials

        try:
            service = build('calendar', 'v3', credentials=credentials)
            events = service.events().list(calendarId='primary').execute()
            return Response({'events': events.get('items', [])})
        except HttpError as e:
            return Response({'error': str(e)})