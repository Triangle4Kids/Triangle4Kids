from django.core.management.base import BaseCommand
from django.conf import settings
import os.path
from django.core.files import File
from core.scrapelib.biz_cparent import CParentBizScraper


def get_path(file):
    return os.path.join(settings.BASE_DIR, 'initial_data', file)


class Command(BaseCommand):
    help = "Run web scraping for all targets"

    def handle(self, *args, **options):
        print("Run web scraping for all targets")
        CParentBizScraper().Run()
