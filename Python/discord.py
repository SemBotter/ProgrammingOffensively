import discord
import os
# import aiofiles
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

GUILD_ID = discord.Object(id=1334245381814620242)

class Client(commands.Bot):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

        try: 
            guild = discord.Object(id=1334245381814620242)
            synced = await self.tree.sync(guild=guild)
            print(f'Synced {len(synced)} commands to guild {guild.id}')

        except Exception as e:
            print(f'Error syncing commands: {e}')

    async def on_message(self, message):
        if message.author == self.user:
            return
        
        if message.content.startswith('hello'):
            await message.channel.send(f'Hou je kanis, {message.author}!')

        if 'bek' in message.content:
            await message.channel.send(f'Nee, jij bent een bek!')


client = Client(command_prefix='!', intents=intents)

@client.tree.command(name='help', description='I cant help you', guild=GUILD_ID)
async def sayHelp(interaction: discord.Interaction):
    await interaction.response.send_message('Too bad')

@client.tree.command(name='embed', description='Embed demo', guild=GUILD_ID)
async def printer(interaction: discord.Interaction):
    embed = discord.Embed(title='SmolGeorgie Github', url='https://github.com/smolgeorgie', description='My github page! Check it out!', color=discord.Color.green())
    embed.set_thumbnail(url='https://cdn.pixabay.com/photo/2022/01/30/13/33/github-6980894_1280.png')
    embed.add_field(name='Repo', value='Star my repositories!', inline=True)
    embed.add_field(name='Follow', value='Follow me on github!')
    embed.set_author(name=interaction.user.name)
    await interaction.response.send_message(embed=embed)

class View(discord.ui.View):
    @discord.ui.button(label='Click me', style=discord.ButtonStyle.green, emoji='🫥')
    async def button_callback(self, button, interaction):
        await button.response.send_message('You have clicked the button')
    
@client.tree.command(name='button', description='Ugly button', guild=GUILD_ID)
async def myButton(interaction: discord.Interaction):
    await interaction.response.send_message(view=View())


token = os.getenv('DISCORD_BOT_TOKEN')
client.run(token)