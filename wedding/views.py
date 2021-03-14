from guests.models import Party
from django.conf import settings
from django.shortcuts import render
from guests.invitation import guess_party_by_invite_id_or_404
from guests.models import Party


def home(request):
    print(request.GET.get("invite_id"))
    party = guess_party_by_invite_id_or_404(request.GET.get("invite_id", 0))
    return render(request, 'home.html', context={
        'party': party,
        'support_email': settings.DEFAULT_WEDDING_REPLY_EMAIL,
    })
