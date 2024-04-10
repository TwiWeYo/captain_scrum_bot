import random
from collections import deque
from utils import get_channel, get_channel_byname, joy_prefix, sad_prefix

random_memory = 10
random_history = dict([])
prev_choices = dict([])


def choose_member(guild, members):
    probabilities = {m: 1 for m in members}
    if not guild in random_history:
        random_history[guild] = deque([])

    r_hist = random_history[guild]
    for h in r_hist:
        if h in probabilities:
            probabilities[h] /= 2
            
    if (guild in prev_choices):
        probabilities[prev_choices[guild]] = 0

    p = []
    v = []
    for val, pr in probabilities.items():
        v.append(val)
        p.append(pr)

    chosen_one = random.choices(v, p)[0]
    # очищаем из памяти тех, кого давно запомнили
    while len(r_hist) >= random_memory:
        r_hist.popleft()
    # добавляем сегодняшнего счастливчика
    r_hist.append(chosen_one)

    prev_choices[guild] = chosen_one

    return chosen_one


async def choose_random_command(message, ch_name = None):

    if ch_name:
        channel = await get_channel_byname(message, ch_name)
    else:
        channel = await get_channel(message)

    if not channel:
        return

    members = channel.members
    if not members:
        await message.channel.send(f'{sad_prefix()} в канале "{channel.name}" никого нет')
        return

    await message.channel.send(joy_prefix().format(choose_member(message.guild, members).mention))
