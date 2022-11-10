# -*- coding: utf-8 -*-

import locale
import random
import re
import requests

from constants import who, who_quotes, weather_codes
from datetime import datetime
from telegram import ParseMode


locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')


def info(update, context):
    answer = f"Вероятность составляет: {random.randrange(100)}%"
    update.message.reply_text(answer)


def stats(update, context):
    username = update.message.from_user.username

    if 'users' not in context.chat_data:
        context.chat_data['users'] = {}

    if username not in context.chat_data['users']:
        context.chat_data['users'][username] = {
            'name': '',
            'messages': 0,
            'words': 0
        }

    context.chat_data['users'][username]['messages'] += 1
    context.chat_data['users'][username]['words'] += len(update.message.text)


def top(update, context):
    data = list(context.chat_data['users'].items())
    sorted_data = sorted(data, key=lambda x: x[1]['words'], reverse=True)

    answer = '`Топ (символы / сообщения):\n\n'
    for i, (user, data) in enumerate(sorted_data):
        answer += f"{i+1}) {user}: {data['words']} / {data['messages']}\n"
    answer += '`'
    update.message.reply_text(
        answer, quote=False, parse_mode=ParseMode.MARKDOWN
    )


def weather(update, context):
    city = re.sub('Царь.*погода', '', update.message.text, flags=re.I)
    city = city.strip().lower()

    nominatim_url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": city,
        "format": "json",
        "limit": 1,
        "accept-language": "russian"
    }

    result = requests.get(nominatim_url, params=params).json()
    lat = result[0]['lat']
    lon = result[0]['lon']

    weather_url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": {
            "temperature_2m_max",
            "temperature_2m_min",
            "weathercode",
            "sunrise",
            "sunset",
            "apparent_temperature_max",
            "apparent_temperature_min"
        },
        "timezone": "auto",
        "timeformat": "unixtime"
    }

    result = requests.get(weather_url, params=params).json()
    daily = result["daily"]

    answer = '`'
    answer += f"{city.capitalize()}\n\n"

    min = daily['temperature_2m_min'][0]
    max = daily['temperature_2m_max'][0]
    feels_min = daily['apparent_temperature_min'][0]
    feels_max = daily['apparent_temperature_max'][0]

    sunrise = datetime.fromtimestamp(daily['sunrise'][0]).strftime('%H:%M')
    sunset = datetime.fromtimestamp(daily['sunset'][0]).strftime('%H:%M')

    answer += f"{'Сейчас: ':<11}{round((min+max)/2)}°C\n"
    answer += f"{'Ощущается: ':<11}{round((feels_min+feels_max)/2)}°C\n"
    answer += f"{'Восход: ':<11}{sunrise}\n"
    answer += f"{'Закат: ':<11}{sunset}\n\n"

    for i, time in enumerate(daily['time']):
        answer += f"{datetime.fromtimestamp(time).strftime('%a, %b %d'):<12} "
        min = daily['temperature_2m_min'][i]
        max = daily['temperature_2m_max'][i]
        code = weather_codes[daily['weathercode'][i]][1]
        answer += f"{code}{round((min+max)/2):>3}°C\n"

    answer += '`'

    update.message.reply_text(
        answer, quote=False, parse_mode=ParseMode.MARKDOWN
    )


def whoami(update, context):
    extension = random.choice(who[2]) if random.randrange(3) == 2 else ''

    name = extension['0'] + ' ' if '0' in extension else ''
    name += random.choice(who[0]) + ' ' + random.choice(who[1])
    name += ' ' + extension['1'] if '1' in extension else ''

    username = update.message.from_user.username
    context.chat_data['users'][username]['name'] = name
    answer = f"@{username}, вы — {name}"
    update.message.reply_text(answer, quote=False)


def whois(update, context):
    who = re.sub('Царь.*кто', '', update.message.text, flags=re.I)
    who = who.replace('?', '').strip().lower()
    who = random.choice(who_quotes) + ' ' + who + ' - @'
    who += random.choice(list(context.chat_data['users'].keys()))
    update.message.reply_text(who.capitalize(), quote=False)


def names(update, context):
    answer = ''
    for user, data in context.chat_data['users'].items():
        if data['name']:
            answer += f"*{user}* - {data['name']}\n"
    update.message.reply_text(
        answer, quote=False, parse_mode=ParseMode.MARKDOWN
    )

