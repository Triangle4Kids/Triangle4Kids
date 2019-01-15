import os.path
from django.core.files import File
from core.scrapelib.event_cparent import CParentEventScraper


def get_path(file):
    return os.path.join(settings.BASE_DIR, 'initial_data', file)


class Command(BaseCommand):
    help = "Run web scraping for all event targets"

    def handle(self, *args, **options):
        print("Run web scraping for all event targets")
        CParentEventScraper().Run()