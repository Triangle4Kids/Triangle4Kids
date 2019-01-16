from django.core.management.base import BaseCommand
from django.conf import settings
import os.path
from django.core.files import File
from core.mapboxlib.latlong import BizLatLong


def get_path(file):
    return os.path.join(settings.BASE_DIR, 'initial_data', file)


class Command(BaseCommand):
    help = "Update all missing business lat/long positions."

    def handle(self, *args, **options):
        print("Updating all business lat/long")
        BizLatLong().Run()