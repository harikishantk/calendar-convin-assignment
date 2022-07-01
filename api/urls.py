from django.urls import path
from api.views import GoogleCalendarInitView, GoogleCalendarRedirectView

urlpatterns = [
    path('init/', GoogleCalendarInitView, name='GoogleCalendarInitView'),
    path('redirect/', GoogleCalendarRedirectView, name='GoogleCalendarRedirectView'),
]