from django.contrib import admin
from .models import Guest, Party


class GuestInline(admin.TabularInline):
    model = Guest
    fields = ('first_name', 'last_name', 'email', 'is_attending', 'diet',
              'whatsapp_inviter')
    readonly_fields = ('first_name', 'last_name', 'email')


class PartyAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'save_the_date_sent',
                    'invitation_sent', 'is_invited_to_church',
                    'invitation_opened', 'is_invited', 'is_attending')
    list_filter = (
        'category',
        'is_invited',
        'is_attending',
        'is_invited_to_church',
        'invitation_opened',
    )
    inlines = [GuestInline]


class GuestAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'party', 'email',
                    'is_attending', 'diet', 'phone_number', 'whatsapp_inviter')
    list_filter = ('is_attending', 'diet', 'party__is_invited',
                   'party__category', 'party__is_invited_to_church',
                   'whatsapp_inviter')


admin.site.register(Party, PartyAdmin)
admin.site.register(Guest, GuestAdmin)
