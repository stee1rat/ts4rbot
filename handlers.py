import random
from constants import who


def whoami(update, context):
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

