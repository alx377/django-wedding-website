from email.mime.image import MIMEImage
import os
from datetime import datetime
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.urls import reverse
from django.http import Http404
from django.template.loader import render_to_string
from guests.models import Guest, Party
if settings.DEBUG:
    import pywhatkit

INVITATION_TEMPLATE = 'guests/email_templates/invitation.html'


def guess_party_by_invite_id_or_404(value):
    try:
        return Party.objects.get(invitation_id=value)
    except Party.DoesNotExist:
        try:
            return Party.objects.get(name=value)
        except Party.DoesNotExist:
            raise Http404()


def get_invitation_context(party):
    return {
        'title': "Kutsu hääjuhlaan",
        'main_image': 'email2.jpg',
        'main_color': '#fff3e8',
        'font_color': '#666666',
        'page_title': "Aleksi ja Marika - Olet kutsuttu!",
        'preheader_text': "Olet kutsuttu!",
        'invitation_id': party.invitation_id,
        'party': party,
    }


def send_invitation_email(party, test_only=False, recipients=None):
    if recipients is None:
        recipients = party.guest_emails
    if not recipients:
        print('===== WARNING: no valid email addresses found for {} ====='.
              format(party))
        return False

    context = get_invitation_context(party)
    context['email_mode'] = True
    context['site_url'] = settings.WEDDING_WEBSITE_URL
    context['couple'] = settings.BRIDE_AND_GROOM
    template_html = render_to_string(INVITATION_TEMPLATE, context=context)
    template_text = "Olet kutsuttu Aleksin ja Marikan häihin. Nähdäksesi tämän kutsun navigoi itsisi tähän osoitteeseen: {}.".format(
        reverse('invitation', args=[context['invitation_id']]))
    subject = "Olet kutsuttu"
    # https://www.vlent.nl/weblog/2014/01/15/sending-emails-with-embedded-images-in-django/
    msg = EmailMultiAlternatives(
        subject,
        template_text,
        settings.DEFAULT_WEDDING_FROM_EMAIL,
        recipients,
        cc=settings.WEDDING_CC_LIST,
        reply_to=[settings.DEFAULT_WEDDING_REPLY_EMAIL])
    msg.attach_alternative(template_html, "text/html")
    msg.mixed_subtype = 'related'
    for filename in (context['main_image'], ):
        attachment_path = os.path.join(os.path.dirname(__file__), 'static',
                                       'invitation', 'images', filename)
        with open(attachment_path, "rb") as image_file:
            msg_img = MIMEImage(image_file.read())
            msg_img.add_header('Content-ID', '<{}>'.format(filename))
            msg.attach(msg_img)

    print(msg.__dict__)
    print('sending invitation to {} ({})'.format(party.name,
                                                 ', '.join(recipients)))
    if not test_only:
        msg.send()
    return True


def send_invitation_whatsapp(party: Party):
    if not settings.DEBUG:
        return
    guest: Guest
    print(party)
    for guest in party.guest_set.all():
        # If already sent invitation skip
        print(guest)
        if guest.invitation_sent:
            continue
        if guest.phone_number:
            print('phone_number: ', guest.phone_number)
            now = datetime.now()
            message = f"""
Olet kutsuttu hääjuhlaamme 07.08.2021!
vp. 31.5.2021
Vastaa kutsuun osoitteessa: {settings.WEDDING_WEBSITE_URL}/invite/{party.invitation_id}
Lisä informaatioa osoitteessa {settings.WEDDING_WEBSITE_URL}?invite_id={party.invitation_id}
Ystävällisin terveisin: Aleksi ja Marika!
            """
            pywhatkit.sendwhatmsg(guest.phone_number, message, now.hour,
                                  now.minute + 1)
            guest.invitation_sent = datetime.now()
            guest.save()
        else:
            return False
    return True


def send_all_invitations(test_only, mark_as_sent, sender):

    to_send_to = Party.in_default_order().filter(
        is_invited=True, invitation_sent=None,
        guest__whatsapp_inviter=sender).exclude(is_attending=False)
    for party in to_send_to:
        succeeded = send_invitation_whatsapp(party)
        # succeeded = send_invitation_email(party, test_only=test_only)
        if mark_as_sent and succeeded:
            party.invitation_sent = datetime.now()
            party.save()
