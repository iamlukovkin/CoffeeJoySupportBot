import os
import logging

from .bot import bot
from django.conf import settings

from . import handlers

handlers.handler()

def main():
    os.system(command='kill -9 $(lsof -t -i:9123)')
    logging.basicConfig(level=logging.INFO)
    bot.polling()
    # bot.send_message(
    #     chat_id=settings.DEV_TG_ID, 
    #     text='Bot is working!'
    #     )
