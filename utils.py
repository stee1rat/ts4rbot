import urllib.request
import json

from fake_headers import Headers


def balaboba(query, intro):
    headers = Headers().generate()
    API_URL = 'https://zeapi.yandex.net/lab/api/yalm/text3'
    payload = {"query": query, "intro": intro, "filter": 1}
    params = json.dumps(payload).encode('utf8')
    req = urllib.request.Request(API_URL, data=params, headers=headers)
    response = urllib.request.urlopen(req)
    return json.loads(response.read().decode('utf8'))['text']


def remove_job_if_exists(name, context):
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True

