import discord
import os
import random

guildname = 'talking scientific pizza'
intents = discord.Intents.all()
client = discord.Client(intents=intents)
tsp = []

prefixes = ['увы, но', 'вынужден огорчить, господа, но', 'вот незадача,', 'бесконечно извиняюсь, но', 'как ни прескорбно, но', 'сожалею, но именно сегодня', 'так уж вышло, что']


def prefix():
    return random.choice(prefixes)


async def choise_random(message):
    global tsp

    args = message.content.split()
    channel_name = 'основной' if len(args) < 2 else args[1]

    channel = [x for x in tsp.channels if x.name.lower() == channel_name and str(x.type) == 'voice']
    if not channel:
        await message.channel.send(f'{prefix()} голосовой канал "{channel_name}" найти не удалось')
        return

    members = channel[0].members
    if not members:
        await message.channel.send(f'{prefix()} в канале "{channel_name}" никого нет')
        return

    await message.channel.send(f'счастливый случай выбрал {random.choice(members).mention}')


@client.event
async def on_ready():
    global tsp
    print('We have logged in as {0.user}'.format(client))

    tsp = [x for x in client.guilds if x.name == guildname][0]


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!random'):
        await choise_random(message)
        

client.run(os.environ['TOKEN'])
