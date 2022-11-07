import logging
import re
import settings

from handlers import whoami
from telegram.ext import Filters, MessageHandler, Updater

logging.basicConfig(filename='bot.log',
                    level=logging.INFO,
                    format=settings.LOGGING_FORMAT)


def main():
    updater = Updater(settings.API_KEY, use_context=True)

    updater.dispatcher.add_handler(
        MessageHandler(
            Filters.regex(re.compile("(?i)(Царь.*кто я.*)", re.IGNORECASE)),
            whoami
        )
    )

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
