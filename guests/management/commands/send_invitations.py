from optparse import make_option
from django.core.management import BaseCommand
# from guests import csv_import
from guests.invitation import send_all_invitations
# from guests.save_the_date import send_all_save_the_dates, clear_all_save_the_dates


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--sender',
                            type=str,
                            help="Who is sending invitation")

    def handle(self, *args, **options):
        # if options['reset']:
        #     clear_all_save_the_dates()
        sender = options['sender']
        if sender not in ["aleksi", "marika"]:
            print("unknown sender try aleksi or marika")
            return
        send_all_invitations(test_only=False, mark_as_sent=True, sender=sender)
