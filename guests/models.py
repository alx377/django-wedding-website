from __future__ import unicode_literals
import datetime
import uuid

from django.db import models
from django.dispatch import receiver

# these will determine the default formality of correspondence
ALLOWED_TYPES = [
    ('formal', 'formal'),
    ('fun', 'fun'),
    ('dimagi', 'dimagi'),
]


def _random_uuid():
    return uuid.uuid4().hex


class Party(models.Model):
    """
    A party consists of one or more guests.
    """
    name = models.TextField()
    category = models.CharField(max_length=20, null=True, blank=True)
    save_the_date_sent = models.DateTimeField(null=True,
                                              blank=True,
                                              default=None)
    save_the_date_opened = models.DateTimeField(null=True,
                                                blank=True,
                                                default=None)
    invitation_id = models.CharField(max_length=32,
                                     db_index=True,
                                     default=_random_uuid,
                                     unique=True)
    invitation_sent = models.DateTimeField(null=True, blank=True, default=None)
    invitation_opened = models.DateTimeField(null=True,
                                             blank=True,
                                             default=None)
    is_invited = models.BooleanField(default=False)
    is_invited_to_church = models.BooleanField(default=False)
    is_attending = models.NullBooleanField(default=None)
    comments = models.TextField(null=True, blank=True)

    def __str__(self):
        return 'Party: {}'.format(self.name)

    @classmethod
    def in_default_order(cls):
        return cls.objects.order_by('category', '-is_invited',
                                    '-is_invited_to_church', 'name')

    @property
    def ordered_guests(self):
        return self.guest_set.order_by('pk')

    @property
    def any_guests_attending(self):
        return any(self.guest_set.values_list('is_attending', flat=True))

    @property
    def guest_emails(self):
        return list(
            filter(None, self.guest_set.values_list('email', flat=True)))


class Guest(models.Model):
    """
    A single guest
    """
    INVITER_CHOICES = (("aleksi", "aleksi"), ("marika", "marika"))
    party = models.ForeignKey('Party', on_delete=models.CASCADE)
    first_name = models.TextField()
    last_name = models.TextField(null=True, blank=True)
    email = models.TextField(null=True, blank=True)
    is_attending = models.NullBooleanField(default=None)
    diet = models.CharField(max_length=255, null=True, blank=True)
    invitation_sent = models.DateTimeField(null=True, blank=True, default=None)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    whatsapp_inviter = models.CharField(max_length=255,
                                        choices=INVITER_CHOICES,
                                        null=True,
                                        blank=True)

    @property
    def name(self):
        return u'{} {}'.format(self.first_name, self.last_name)

    @property
    def unique_id(self):
        # convert to string so it can be used in the "add" templatetag
        return str(self.pk)

    def __str__(self):
        return 'Guest: {} {}'.format(self.first_name, self.last_name)
