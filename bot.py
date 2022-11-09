# -*- coding: utf-8 -*-

import logging
import re
import settings

from handlers import whoami, whois, info, weather, whostats, stats

from telegram import Update
from telegram.ext import (
    Filters, MessageHandler, TypeHandler, Updater, PicklePersistence
)

logging.basicConfig(filename='bot.log',
                    level=logging.INFO,
                    format=settings.LOGGING_FORMAT)


def main():
    db = PicklePersistence(filename='bot.db')

    updater = Updater(settings.API_KEY, use_context=True, persistence=db)
    updater.dispatcher.add_handler(TypeHandler(Update, stats), -1)

    updater.dispatcher.add_handler(
        MessageHandler(
            Filters.regex(re.compile("(?i)(Царь.*кто все( |\?)*$)",
                          re.IGNORECASE)),
            whostats
        )
    )

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
            Filters.regex(re.compile("(?i)(Царь.*(инфа|вероятность).*)", 
                          re.IGNORECASE)),
            info
        )
    )

    updater.dispatcher.add_handler(
        MessageHandler(
            Filters.regex(re.compile("(?i)(Царь.*погода.*)", re.IGNORECASE)),
            weather
        )
    )

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
