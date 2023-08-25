import telebot

from . import repository

BOT_TOKEN = '6599693641:AAFWNdc9DFWYNJ-GaB2rvhB7-OCxvC9IYi4'

bot = telebot.TeleBot(token=BOT_TOKEN)
db_path = './db.sqlite3'
