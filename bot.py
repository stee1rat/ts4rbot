# -*- coding: utf-8 -*-

import logging
import re

from settings import API_KEY, BOT_NAME, LOGGING_FORMAT

from handlers import (
    anecdote, apod, fact, info, weather, names, instruction,
    stats, top, today, quiz, quiz_answer, quiztop, whoami, whois,
)

from telegram import Update
from telegram.ext import (
    CallbackQueryHandler, CommandHandler, Filters,
    MessageHandler, PicklePersistence, TypeHandler, Updater
)

logging.basicConfig(filename='bot.log',
                    level=logging.INFO,
                    format=LOGGING_FORMAT)


def main():
    db = PicklePersistence(filename='bot.db')

    updater = Updater(API_KEY, use_context=True, persistence=db)
    updater.dispatcher.add_handler(TypeHandler(Update, stats), -1)

    updater.dispatcher.add_handler(CallbackQueryHandler(quiz_answer))

    updater.dispatcher.add_handler(CommandHandler('anecdote', anecdote))
    updater.dispatcher.add_handler(CommandHandler('apod', apod))
    updater.dispatcher.add_handler(CommandHandler('fact', fact))
    updater.dispatcher.add_handler(CommandHandler('quiztop', quiztop))
    updater.dispatcher.add_handler(CommandHandler('quiz', quiz))
    updater.dispatcher.add_handler(CommandHandler('top', top))
    updater.dispatcher.add_handler(CommandHandler('today', today))
    updater.dispatcher.add_handler(CommandHandler('whoami', whoami))
    updater.dispatcher.add_handler(CommandHandler('names', names))

    updater.dispatcher.add_handler(
        MessageHandler(
            Filters.regex(
                re.compile(f"(?i)({BOT_NAME}.*анекдот.*)", re.IGNORECASE)),
            anecdote
        )
    )

    updater.dispatcher.add_handler(
        MessageHandler(
            Filters.regex(
                re.compile(f"(?i)({BOT_NAME}.*факт.*)", re.IGNORECASE)),
            fact
        )
    )

    updater.dispatcher.add_handler(
        MessageHandler(
            Filters.regex(re.compile(f"(?i)({BOT_NAME}.*кто все( |\?)*$)",
                          re.IGNORECASE)),
            names
        )
    )

    updater.dispatcher.add_handler(
        MessageHandler(
            Filters.regex(
                re.compile(f"(?i)({BOT_NAME}.*кто я.*)",
                           re.IGNORECASE)),
            whoami
        )
    )

    updater.dispatcher.add_handler(
        MessageHandler(
            Filters.regex(
                re.compile(f"(?i)({BOT_NAME}.*кто.*)",
                           re.IGNORECASE)),
            whois
        )
    )

    updater.dispatcher.add_handler(
        MessageHandler(
            Filters.regex(
                re.compile(f"(?i)({BOT_NAME}.*(инфа|вероятность).*)",
                           re.IGNORECASE)),
            info
        )
    )

    updater.dispatcher.add_handler(
        MessageHandler(
            Filters.regex(
                re.compile(f"(?i)({BOT_NAME}.*погода.*)",
                           re.IGNORECASE)),
            weather
        )
    )

    updater.dispatcher.add_handler(
        MessageHandler(
            Filters.regex(
                re.compile(f"(?i)({BOT_NAME}.*инструкция.*)",
                           re.IGNORECASE)),
            instruction,
            run_async=True
        )
    )

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
