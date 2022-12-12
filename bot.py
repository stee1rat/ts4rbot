# -*- coding: utf-8 -*-

import logging

from handlers import (anecdote, apod, choose, fact, film, info, instruction,
                      names, quiz, quiz_answer, quiztop, recipe, stats, today,
                      top, weather, whoami, whois, wiki, wisdom)
from settings import API_KEY, LOGGING_FORMAT
from utils import getMessageHandler
from telegram import Update
from telegram.ext import (CallbackQueryHandler, CommandHandler,
                          PicklePersistence, TypeHandler, Updater)

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

    updater.dispatcher.add_handler(getMessageHandler("выбери", choose, True))
    updater.dispatcher.add_handler(getMessageHandler("кто все", names))
    updater.dispatcher.add_handler(getMessageHandler("кто я", whoami))
    updater.dispatcher.add_handler(getMessageHandler("кто", whois))
    updater.dispatcher.add_handler(
        getMessageHandler("(инфа|вероятность)", info))

    updater.dispatcher.add_handler(getMessageHandler("погода", weather))

    updater.dispatcher.add_handler(
        getMessageHandler("инструкция", instruction, True))

    updater.dispatcher.add_handler(getMessageHandler("рецепт", recipe, True))
    updater.dispatcher.add_handler(getMessageHandler("мудрость", wisdom, True))
    updater.dispatcher.add_handler(getMessageHandler("что такое", wiki, True))
    updater.dispatcher.add_handler(getMessageHandler("фильм", film, True))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
