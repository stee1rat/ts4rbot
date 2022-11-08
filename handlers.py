# -*- coding: utf-8 -*-

import random
import re

from constants import who, who_quotes


def whoami(update, context):
    save_username(update, context)
    answer = f"@{update.message.from_user.username}, вы — "
    
    if random.choice([0, 1, 2]) == 2:
        extension = random.choice(who[2])
    else:
        extension = ''

    if '0' in extension:
        answer += extension['0'] + ' '

    answer += random.choice(who[0]) + ' ' + random.choice(who[1])

    if '1' in extension:
        answer += ' ' + extension['1']

    update.message.reply_text(answer, quote=False)


def info(update, context):
    save_username(update, context)
    answer = f"Вероятность составляет: {random.randrange(100)}%"
    update.message.reply_text(answer)


def save_username(update, context):
    if 'users' not in context.chat_data:
        context.chat_data['users'] = []
    if update.message.from_user.username not in context.chat_data['users']:
        context.chat_data['users'].append(update.message.from_user.username)


def whois(update, context):
    save_username(update, context)
    who = re.sub('Царь.*кто', '', update.message.text, flags=re.I)
    who = who.replace('?','').strip().lower()
    who = random.choice(who_quotes) + ' ' + who + ' - @'
    who += random.choice(context.chat_data['users'])
    update.message.reply_text(who.capitalize(), quote=False)