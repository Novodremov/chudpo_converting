import logging

from dotenv import load_dotenv

load_dotenv()

from chudpo_bot.chudpo_bot import main  # noqa


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
    main()
