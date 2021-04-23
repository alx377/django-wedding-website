from guests.models import Party
from django.conf import settings
from django.shortcuts import render
from guests.invitation import guess_party_by_invite_id_or_404
from guests.models import Party


def home(request):
    print(request.GET.get("name"))
    party = guess_party_by_invite_id_or_404(request.GET.get("name", "asd"))
    return render(request, 'home.html', context={
        'party': party,
        'support_email': settings.DEFAULT_WEDDING_REPLY_EMAIL,
    })
