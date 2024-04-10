import discord

async def scrum_poker_command(message, topic):    
    await message.channel.send(topic, view=VotesView(topic))


async def vote(self, interaction : discord.Interaction, button : discord.ui.Button, votes: dict):
    votes[interaction.user] = int(button.label) if button.label else 0

    await interaction.response.send_message(f'Вы выбрали {votes[interaction.user]}', ephemeral=True)

    await interaction.response.edit_message(view=self)

class VotesView(discord.ui.View):
    def __init__(self, topic):
        super().__init__()
        self.votes = dict([])
        self.topic = topic


    @discord.ui.button(label='3', row=0, style=discord.ButtonStyle.secondary)
    async def vote_3(self, interaction : discord.Interaction, button : discord.ui.Button):
        await vote(self, interaction, button, self.votes)

    @discord.ui.button(label='5', row=0, style=discord.ButtonStyle.secondary)
    async def vote_5(self, interaction : discord.Interaction, button : discord.ui.Button):
        await vote(self, interaction, button, self.votes)

    @discord.ui.button(label='8', row=0, style=discord.ButtonStyle.secondary)
    async def vote_8(self, interaction : discord.Interaction, button : discord.ui.Button):
        await vote(self, interaction, button, self.votes)

    @discord.ui.button(label='13', style=discord.ButtonStyle.secondary)
    async def vote_13(self, interaction : discord.Interaction, button : discord.ui.Button):
        await vote(self, interaction, button, self.votes)

    @discord.ui.button(label='20', row=1, style=discord.ButtonStyle.secondary)
    async def vote_20(self, interaction : discord.Interaction, button : discord.ui.Button):
        await vote(self, interaction, button, self.votes)

    @discord.ui.button(label='40', row=1, style=discord.ButtonStyle.secondary)
    async def vote_40(self, interaction : discord.Interaction, button : discord.ui.Button):
        await vote(self, interaction, button, self.votes)

    @discord.ui.button(label='100', row=1, style=discord.ButtonStyle.secondary)
    async def vote_100(self, interaction : discord.Interaction, button : discord.ui.Button):
        await vote(self, interaction, button, self.votes)

    @discord.ui.button(label = 'Завершить', row=0, style=discord.ButtonStyle.danger)
    async def button_callback_finish(self, interaction : discord.Interaction, button : discord.ui.Button):
        for child in self.children:
            child.disabled = True

        average = 0
        for user in self.votes:
            username = user.nick if user.nick else user.name
            await interaction.channel.send(f'{username} - {self.votes[user]}')
            average += self.votes[user]

        average /= len(self.votes)
        await interaction.channel.send(f'Голосование ***"{self.topic}"*** завершено.\nСреднее арифметическое: **{round(average, 2)}**\nСреднее глазометрическое: **{round(average)}**')

        await interaction.response.edit_message(view=self)
