import discord
from discord.ext import commands

from slash_commands.choose_random import choose_random_command
from slash_commands.scrum_poker import scrum_poker_command

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command(name='Рандом', description='дом дом мой милый рандом', aliases=['random', 'рандом'])
async def choose_random(ctx, name = None):
    await choose_random_command(ctx.message, name)

@bot.command(aliases=['vote', 'poker', 'покер'])
async def scrum_poker(ctx, *, topic):
    await scrum_poker_command(ctx, topic)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def ping(ctx: commands.Context):
    await ctx.send('Pong!')

bot.run('TOKEN')