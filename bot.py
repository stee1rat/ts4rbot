# -*- coding: utf-8 -*-

import logging
import re
import settings

from handlers import (
    whoami, whois, info, weather, names, stats, top, quiz, quiz_answer,
    quiztop
)

from telegram import Update
from telegram.ext import (
    Filters, MessageHandler, TypeHandler, Updater, PicklePersistence,
    CallbackQueryHandler, CommandHandler
)

logging.basicConfig(filename='bot.log',
                    level=logging.INFO,
                    format=settings.LOGGING_FORMAT)


def main():
    db = PicklePersistence(filename='bot.db')

    updater = Updater(settings.API_KEY, use_context=True, persistence=db)
    updater.dispatcher.add_handler(TypeHandler(Update, stats), -1)

    updater.dispatcher.add_handler(CallbackQueryHandler(quiz_answer))

    updater.dispatcher.add_handler(CommandHandler('quiztop', quiztop))
    updater.dispatcher.add_handler(CommandHandler('quiz', quiz))
    updater.dispatcher.add_handler(CommandHandler('top', top))
    updater.dispatcher.add_handler(CommandHandler('whoami', whoami))
    updater.dispatcher.add_handler(CommandHandler('names', names))

    updater.dispatcher.add_handler(
        MessageHandler(
            Filters.regex(re.compile("(?i)(Царь.*кто все( |\?)*$)",
                          re.IGNORECASE)),
            names
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
