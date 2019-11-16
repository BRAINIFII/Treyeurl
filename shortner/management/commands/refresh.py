from django.core.management.base import BaseCommand, CommandError

from shortner.models import TreyeURL

class Command(BaseCommand):
    help = 'Refreshes all TreyeURL Shortcodes'

    def add_arguments(self, parser):
        parser.add_argument('--items', type=int)

    def handle(self, *args, **options):
        return TreyeURL.objects.refresh_shortcodes(items=options['items'])