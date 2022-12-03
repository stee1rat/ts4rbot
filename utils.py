import json
import urllib.request

import requests

def remove_job_if_exists(name, context):
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


def balaboba(query, intro):
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4) AppleWebKit/605.1.15 '
                    '(KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
        'Origin': 'https://yandex.ru',
        'Referer': 'https://yandex.ru/',
    }
    API_URL = 'https://zeapi.yandex.net/lab/api/yalm/text3'
    payload = {"query": query, "intro": intro, "filter": 1}

    payload = json.dumps({
        "filter": 0,
        "intro": 11, # мудрость
        "query": query
    })

    payload = json.dumps({
        "filter": 0,
        "intro": 24, # инструкция
        "query": query
    })

    
    payload = json.dumps({
        "filter": 0,
        "intro": 25, # рецепты
        "query": query
    })

    payload = json.dumps({
        "filter": 0,
        "intro": intro,
        "query": query
    })



    r = requests.request("POST", API_URL, headers=headers, data=payload)
    return json.loads(r.text)['text']
