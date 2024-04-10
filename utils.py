import random

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

def sad_prefix():
    return random.choice(sad_prefixes)


def joy_prefix():
    return random.choice(joy_prefixes)

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