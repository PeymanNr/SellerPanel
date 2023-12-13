# your_app/management/commands/crawl.py
from django.core.management.base import BaseCommand

from product.crawler import LinkCrawler


class Command(BaseCommand):
    help = 'Run the crawler'

    def handle(self, *args, **options):
        # Create an instance of your crawler
        crawler = LinkCrawler()

        # Run the crawler
        crawler.start()

        self.stdout.write(self.style.SUCCESS('Crawler executed successfully'))
