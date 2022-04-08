import discord
import random
from collections import deque

intents = discord.Intents.all()
client = discord.Client(intents=intents)

sad_prefixes = ['увы, но', 'вынужден огорчить, господа, но', 'вот незадача,',
                'бесконечно извиняюсь, но', 'как ни прискорбно, но',
                'сожалею, но именно сегодня', 'так уж вышло, что']
joy_prefixes = ['счастливый случай выбрал {}',
                'перенаправляем прожекторы... всё внимание на {}!',
                'поздравляю! самый счастливый человек сегодня — {}',
                'герой сегодняшнего дня — {}', 'а самый красивый голос в канале — у {}, вот послушайте',
                'как ни крутись, но тут без {} не обойтись', 'победитель розыгрыша — {}',
                'человек-легенда, лауреат премии "их выбрал рандом" — {}',
                'случайности не случайны, {} знает это, как никто другой',
                'к микрофону приглашается MVP этого дня — {}',
                'рецепт отличного дня: кофе + радуга + {}',
                'сколько бота не корми, он всё равно на {} смотрит',
                'here we go again (c) {}',
                'вышел месяц из тумана, вынул ножик из кармана: "буду резать, буду бить, всё равно {} водить"',
                'и премия "ЗОТОЙ СТЕНДАПОФОН" вручается... {}!',
                'May the Force be with {}',
                'Моя мама всегда говорила: "Жизнь как коробка шоколадных конфет: никогда не знаешь, какая начинка попадётся {}"',
                'А вот и {}!']

random_memory = 10
random_history = dict([])
prev_choices = dict([])

def sad_prefix():
    return random.choice(sad_prefixes)


def joy_prefix():
    return random.choice(joy_prefixes)


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


async def choose_random(message):
    args = message.content.split()

    if len(args) >= 2:
        channel = await get_channel_byname(message, args[1])
    else:
        channel = await get_channel(message)

    if not channel:
        return

    members = channel.members
    if not members:
        await message.channel.send(f'{sad_prefix()} в канале "{channel.name}" никого нет')
        return

    await message.channel.send(joy_prefix().format(choose_member(message.guild, members).mention))


async def get_channel(message):
    guild = message.guild
    channel = [x for x in guild.channels if str(x.type) == 'voice' and message.author in x.members]
    if not channel:
        await message.channel.send(f'{sad_prefix()} {message.author.mention} не удалось найти ни в одном из каналов')
        return
    return channel[0]


async def get_channel_byname(message, ch_name):
    guild = message.guild
    channel = [x for x in guild.channels if x.name.lower() == ch_name and str(x.type) == 'voice']
    if not channel:
        await message.channel.send(f'{sad_prefix()} голосовой канал "{ch_name}" найти не удалось')
        return
    return channel[0]


@client.event
async def on_ready():
    global tsp
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower().startswith('!random') or message.content.lower().startswith('!рандом'):
        await choose_random(message)


client.run('TOKEN')
