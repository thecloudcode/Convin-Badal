from django.urls import path, include
from calendar_api.views import GoogleCalendarInitView, GoogleCalendarRedirectView

urlpatterns = [
    path('', GoogleCalendarInitView.as_view(), name='home'),  # Add this line
    path('rest/v1/calendar/init/', GoogleCalendarInitView.as_view(), name='calendar-init'),
    path('rest/v1/calendar/redirect/', GoogleCalendarRedirectView.as_view(), name='calendar-redirect'),
]
