import telebot

from telebot.types import InlineKeyboardButton
from telebot.types import InlineKeyboardMarkup
from telebot.types import Message
from telebot.types import CallbackQuery

from .bot import bot, db_path
from . import repository
from . import message_text
from . import functions


def cmd_start(message: Message):
    user_id = message.chat.id
    check_user = repository.check_user(
        db_path=db_path,
        table_name='Code_users',
        check_graph='telegram_id',
        param_to_check=user_id
    )
    try:
        nickname = message.from_user.username
    except Exception as e:
        nickname = None
    username = message.from_user.full_name
    if not check_user:
        repository.insert_row(
            db_path=db_path,
            table_name='Code_users',
            telegram_id = user_id,
            nickname = nickname,
            is_admin = False,
            username = username,
            admin_answered = False,
            answered_to = 0
        )
    bot.send_message(
        chat_id=message.chat.id,
        text=message_text.start_message
    )


def send_message(message: Message):
    user_id = message.chat.id
    row = repository.get_rows_by_value(
        database_path=db_path,
        table_name='Code_users',
        search_column='telegram_id',
        search_value=user_id
    )[0]
    admin_status = row[4]
    is_admin = row[3]
    if (admin_status == 0 and is_admin) or not is_admin:
        repository.insert_row(
            db_path=db_path,
            table_name='Code_messages',
            telegram_id = user_id,
            message = message.text,
            answered_message = ''
        )
        row = repository.get_rows_by_value(
            database_path=db_path,
            table_name='Code_messages',
            search_column='message',
            search_value=message.text
        )
        message_id = row[0][3]
        keyboard = InlineKeyboardMarkup(row_width=1)
        keyboard.add(
            InlineKeyboardButton(
                text='Ответить', 
                callback_data=f'answer_{message_id}'
            )
        )
        admins = functions.get_admins()
        message_analysed = functions.check_message(message.text)
        for message_for_send in message_analysed:
            for admin in admins:
                bot.send_message(
                    chat_id=admin,
                    text='Вам пришло новое сообщение от пользователя: \n\n' + message_for_send,
                    reply_markup=keyboard
                )
        bot.send_message(
            chat_id=message.chat.id,
            text=message_text.message_is_sended
        )
    else:
        message_answered_id = row[-1]
        user_to_send = repository.get_value_by_search(
            database_path=db_path,
            table_name='Code_messages',
            search_column='message_id',
            search_value=message_answered_id,
            target_column='telegram_id'
        )
        repository.update_value(
            database_path=db_path,
            table_name='Code_messages',
            search_column='message_id',
            param_to_search=message_answered_id,
            column_to_change='answered_message',
            new_value=message.text
        )
        repository.update_value(
            database_path=db_path,
            table_name='Code_users',
            search_column='telegram_id',
            param_to_search=user_id,
            column_to_change='answered_to',
            new_value=False
        )
        repository.update_value(
            database_path=db_path,
            table_name='Code_users',
            search_column='telegram_id',
            param_to_search=user_id,
            column_to_change='admin_answered',
            new_value=False
        )
        bot.send_message(
            chat_id=user_to_send,
            text='Вам пришло новое сообщение от поддержки: \n\n' + message.text
        )
        bot.send_message(
            chat_id=user_id,
            text='Ваше сообщение отправлено пользователю'
        )


def answer_message(query: CallbackQuery):
    user_id = query.message.chat.id
    message_id = int(query.data[7:])

    repository.update_value(
        database_path=db_path,
        table_name='Code_users',
        search_column='telegram_id',
        param_to_search=user_id,
        column_to_change='answered_to',
        new_value=message_id
    )
    repository.update_value(
        database_path=db_path,
        table_name='Code_users',
        search_column='telegram_id',
        param_to_search=user_id,
        column_to_change='admin_answered',
        new_value=True
    )
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(
            text='Отмена', 
            callback_data='close'
        )
    )
    bot.send_message(
        chat_id=user_id,
        text=message_text.enter_your_answer,
        reply_markup=keyboard
    )
    

def close_answer(query: CallbackQuery):
    user_id = query.message.chat.id
    repository.update_value(
        database_path=db_path,
        table_name='Code_users',
        search_column='telegram_id',
        param_to_search=user_id,
        column_to_change='answered_to',
        new_value=False
    )
    repository.update_value(
        database_path=db_path,
        table_name='Code_users',
        search_column='telegram_id',
        param_to_search=user_id,
        column_to_change='admin_answered',
        new_value=False
    )
    bot.send_message(
        chat_id=user_id,
        text='Ответ отменен'
    )


def handler():
    bot.register_message_handler(
        callback=cmd_start, 
        commands=['start']
    )
    bot.register_message_handler(
        callback=send_message,
        content_types=['text']
    )
    bot.register_callback_query_handler(
        callback=answer_message,
        func=lambda query: query.data[:7] == 'answer_'
    )
    bot.register_callback_query_handler(
        callback=close_answer,
        func=lambda query: query.data == 'close'
    )
