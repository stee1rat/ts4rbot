# -*- coding: utf-8 -*-

import logging
import re
import settings

from handlers import whoami, save_username, whois, info
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

    updater.dispatcher.add_handler(
        MessageHandler(
            Filters.regex(re.compile("(?i)(Царь.*кто.*)", re.IGNORECASE)),
            whois
        )
    )

    updater.dispatcher.add_handler(
        MessageHandler(
            Filters.regex(re.compile("(?i)(Царь.*инфа.*)", re.IGNORECASE)),
            info
        )
    )

    updater.dispatcher.add_handler(MessageHandler(Filters.text, save_username))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
