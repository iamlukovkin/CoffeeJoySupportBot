from ...bot_config import main

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Telegram Bot'

    def handle(self, *args, **kwargs):
        main.main()

