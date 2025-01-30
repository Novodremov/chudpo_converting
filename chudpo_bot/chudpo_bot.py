import os
import logging
import sys
from datetime import datetime

from telebot import TeleBot, types

from converting.constants import TEST_COLUMNS, WORKER_COLUMNS, XML_NAME_FORMAT
from converting.convert import converting_to_xml
from .exceptions import CovertingError


logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
logger.addHandler(handler)

NECESSARY_COLUMNS = list(WORKER_COLUMNS.values()) + list(TEST_COLUMNS.values())

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
# TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
bot = TeleBot(token=TELEGRAM_TOKEN)
user_states = {}

TEMP_FOLDER = os.path.join(
    os.path.dirname(__file__), '..', 'converting', 'temp')
os.makedirs(TEMP_FOLDER, exist_ok=True)


def check_tokens():
    """Функция проверки наличия необходимых данных в окружении."""
    if not all((TELEGRAM_TOKEN,
                # TELEGRAM_CHAT_ID,
                )):
        token_names = ['TELEGRAM_TOKEN',
                       # 'TELEGRAM_CHAT_ID',
                       ]
        missing_tokens = ', '.join(
            [token for token in token_names if not globals()[token]])
        error = f'Не определены переменные окружения: {missing_tokens}'
        logger.critical(error)
        sys.exit(error)


def create_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_help = types.KeyboardButton('/help')
    button_many = types.KeyboardButton('/many')
    keyboard.add(button_help, button_many)
    return keyboard


@bot.message_handler(commands=['start'])
def handle_start_command(message):
    bot.send_message(message.chat.id,
                     f'Привет, {message.from_user.first_name}! '
                     'Наберите команду /help для помощи',
                     reply_markup=create_keyboard())


@bot.message_handler(commands=['help'])
def handle_help_command(message):
    help_text = ('Загрузите файл в формате xlsx для конвертации в xml. '
                 'В файле обязательны следующие столбцы:\n'
                 f'*{'\n'.join(NECESSARY_COLUMNS)}*\n'
                 'По команде /many можно загрузить несколько файлов сразу.')
    bot.reply_to(message, help_text,
                 parse_mode='Markdown',
                 reply_markup=create_keyboard())


@bot.message_handler(commands=['many'])
def handle_many_command(message):
    user_states[message.chat.id] = []  # Создаём список для хранения файлов
    bot.reply_to(message, 'Отправьте файлы .xlsx для конвертации. '
                          'Пришлите любое текстовое сообщение для завершения.')


@bot.message_handler(content_types=['document'])
def handle_document(message):
    if (
        message.document.mime_type ==
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    ):
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        file_name = message.document.file_name
        temp_file_path = os.path.join(TEMP_FOLDER, file_name)
        with open(temp_file_path, 'wb') as new_file:
            new_file.write(downloaded_file)

        # Проверяем состояние пользователя
        if message.chat.id in user_states:
            # Добавляем файл в список для текущего пользователя
            user_states[message.chat.id].append(temp_file_path)
            bot.reply_to(message, f'Файл {file_name} добавлен. Отправьте ещё '
                                  'файлы или любое текстовое сообщение для '
                                  'завершения.')
        else:
            # Если не в режиме many, сразу конвертируем и отправляем xml
            xml_file_name = f"{os.path.splitext(file_name)[0]}.xml"
            xml_file_path = os.path.join(TEMP_FOLDER, xml_file_name)
            try:
                converting_to_xml([temp_file_path], xml_file_path)
            except Exception as error:
                raise CovertingError(
                    f'Произошла ошибка конвертирования: {error}'
                )
            with open(xml_file_path, 'rb') as xml_file:
                bot.send_document(message.chat.id, xml_file)

            os.remove(temp_file_path)
            os.remove(xml_file_path)
    else:
        bot.reply_to(message, 'Пожалуйста, отправьте файл в формате .xlsx')


@bot.message_handler(func=lambda message: True)
def handle_text_message(message):
    if message.chat.id in user_states:
        # Завершаем прием файлов и конвертируем их в XML
        xlsx_files = user_states[message.chat.id]
        if xlsx_files:
            xml_file_name = f'combined_{
                datetime.now().strftime(XML_NAME_FORMAT)}.xml'
            xml_file_path = os.path.join(TEMP_FOLDER, xml_file_name)
            try:
                converting_to_xml(xlsx_files, xml_file_path)
            except Exception as error:
                raise CovertingError(
                    f'Произошла ошибка конвертирования: {error}'
                )

            with open(xml_file_path, 'rb') as xml_file:
                bot.send_document(message.chat.id, xml_file)

            for file in xlsx_files:
                os.remove(file)
            os.remove(xml_file_path)

        del user_states[message.chat.id]  # Удаляем состояние пользователя
        bot.reply_to(message, 'Конвертация завершена. Файлы отправлены.',
                     reply_markup=create_keyboard())
    else:
        bot.reply_to(message, 'Команда неизвестна. Вызовите команду /help '
                              'для помощи.',
                     reply_markup=create_keyboard())


def main():
    """Запуск бота."""
    check_tokens()
    bot.polling()
