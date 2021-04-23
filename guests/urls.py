from django.conf.urls import url
from django.urls import path

from guests.views import GuestListView, export_guests, \
    invitation,  rsvp_confirm, dashboard

urlpatterns = [
    url(r'^guests/$', GuestListView.as_view(), name='guest-list'),
    url(r'^dashboard/$', dashboard, name='dashboard'),
    url(r'^guests/export$', export_guests, name='export-guest-list'),
    path('invite/<slug:party_name>/', invitation),
    path('rsvp/confirm/<slug:party_name>/', rsvp_confirm, name='rsvp-confirm'),
]
