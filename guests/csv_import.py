import csv
import io
import uuid
from guests.models import Party, Guest
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


def import_guests(path):
    with open(path, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        first_row = True
        for row in reader:
            if first_row:
                first_row = False
                continue
            # yapf: disable
            party_name, first_name, last_name, category, is_invited, is_invited_to_church, email, phone_number, whatsapp_inviter = row[:9]
            # yapf: enable
            if not party_name:
                print('skipping row {}'.format(row))
                continue
            party = Party.objects.get_or_create(name=party_name)[0]
            party.is_invited_to_church = _is_true(is_invited_to_church)
            party.category = category
            party.is_invited = _is_true(is_invited)
            if not party.invitation_id:
                party.invitation_id = uuid.uuid4().hex
            party.save()
            if email:
                guest, created = Guest.objects.get_or_create(party=party,
                                                             email=email)
                guest.first_name = first_name
                guest.last_name = last_name
            if phone_number:
                guest, created = Guest.objects.get_or_create(
                    party=party,
                    phone_number=phone_number,
                    whatsapp_inviter=whatsapp_inviter)
                guest.first_name = first_name
                guest.last_name = last_name
            else:
                guest = Guest.objects.get_or_create(party=party,
                                                    first_name=first_name,
                                                    last_name=last_name)[0]
            guest.save()


def export_guests():
    headers = [
        'party_name', 'first_name', 'last_name', 'category', 'is_invited',
        'is_invited_to_church', 'is_attending', 'diet', 'email',
        'phone_number', 'whatsapp_inviter', 'comments'
    ]
    with open('asd.csv', mode='w') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        for party in Party.in_default_order():
            for guest in party.guest_set.all():
                # if guest.is_attending:
                writer.writerow([
                    party.name,
                    guest.first_name,
                    guest.last_name,
                    party.category,
                    party.is_invited,
                    party.is_invited_to_church,
                    guest.is_attending,
                    guest.diet,
                    guest.email,
                    guest.phone_number,
                    guest.whatsapp_inviter,
                    party.comments,
                ])
        return file


def _is_true(value):
    value = value or ''
    return value.lower() in ('y', 'yes', 'true')
