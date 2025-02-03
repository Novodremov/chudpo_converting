import logging
import os
import sys
import threading
from dotenv import load_dotenv
from PIL import Image
from pystray import MenuItem, Icon, Menu

# Получаем путь к исполняемому файлу или исходному скрипту
BASE_DIR = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
env_path = os.path.join(BASE_DIR, '.env')

load_dotenv(env_path)

from chudpo_bot.chudpo_bot import main  # noqa


def on_quit(icon, item):
    icon.stop()


def setup(icon):
    icon.visible = True


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.WARNING,
        filename='bot.log',
        filemode='w',
        encoding='utf-8',
        format='[{asctime}] #{levelname:8} {filename}:'
               '{lineno} - {name} - {message}',
        style='{',
    )

    # Создание иконки для трея
    icon = Icon('bot_icon')
    icon.icon = Image.open(os.path.join(BASE_DIR, 'logo.png'))
    icon.menu = Menu(MenuItem('Выход', on_quit))
    icon.title = 'ЧУДПО-бот запущен'

    # Запускаем бота в отдельном потоке
    bot_thread = threading.Thread(target=main, daemon=True)
    bot_thread.start()

    icon.run(setup)
