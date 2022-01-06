import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_voice_state_update(member, before, after):
    if not before.channel and after.channel is not None:
        channelTo = None
        guild = discord.utils.find(lambda g: g.id == member.guild.id, client.guilds)
        for channel in guild.channels:
            if str(channel.type) == 'text':
                channelTo = client.get_channel(channel.id)
        await channelTo.send(f'{member.display_name} is now hanging out in {after.channel.name}!')

client.run(TOKEN)