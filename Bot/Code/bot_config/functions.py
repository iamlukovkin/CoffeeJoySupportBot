from telebot import types
from .bot import db_path
from . import repository

def check_message(text_for_message):
    msg_length = len(text_for_message)
    if msg_length >= 4096:
        splitter = []
        while len(text_for_message) != 0:
            index_slayer = 0
            splitter.append(
                text_for_message[
                    index_slayer : index_slayer + 4096
                ]
            )
            text_for_message = text_for_message[4096:]
    else:
        splitter = [text_for_message]
    return splitter


def get_admins():
    rows = repository.get_rows_by_value(
        database_path=db_path,
        table_name='Code_users',
        search_column='is_admin',
        search_value=True
    )

    admin_id = []
    for row in rows:
        admin_id.append(row[-2])
    
    return admin_id

