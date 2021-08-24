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
                'вышел месяц из тумана, вынул ножик из кармана: "буду резать, буду бить, всё равно {} водить"']

random_memory = 10
random_history = dict([])

def sad_prefix():
    return random.choice(sad_prefixes)

def joy_prefix():
  return random.choice(joy_prefixes)

def choise_member(guild, members):
    probabilities = {m: 1 for m in members}
    if not guild in random_history:
        random_history[guild] = deque([])

    r_hist = random_history[guild]
    for h in r_hist:
        if h in probabilities:
            probabilities[h] /= 2

    p = []
    v = []
    for val, pr in probabilities.items():
        v.append(val)
        p.append(pr)
            
    choosen_one = random.choices(v, p)[0]
    # очищаем из памяти тех, кого давно запомнили
    while len(r_hist) >= random_memory:
        r_hist.popleft()
    # добавляем сегодняшнего счастливчика
    r_hist.append(choosen_one)
    return choosen_one

async def choise_random(message):
    args = message.content.split()

    if len(args) >= 2:
        channel = await get_channel_byname(message, args[1])
    else:
        channel = await get_channel(message)
        
    if not channel:
        return

    members = channel.members
    if not members:
        await message.channel.send(f'{sad_prefix()} в канале "{channel_name}" никого нет')
        return

    await message.channel.send(joy_prefix().format(choise_member(message.guild, members).mention))


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
        await choise_random(message)
        

client.run('TOKEN')
