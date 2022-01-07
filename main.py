import os
import mods.db as db
import mods.bot.events as bot_events
import mods.bot.commands as bot_commands
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
#client = discord.Client()


bot = commands.Bot(command_prefix='st ')

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.event
async def on_voice_state_update(member, before, after):

    if bot_events.is_member_joined(before,after):
        toChannel = bot_events.get_channel_to_message(discord, bot, member.guild.id)

        if toChannel is None:
            return

        await toChannel.send(f'`{member.display_name}` is now hanging out in `{after.channel.name}`!', delete_after=300)

        db.add_member_join_event(member.guild.id, member.id, member.display_name)

@bot.command(name='channel', help='Sets the channel for when a member joins a voice channel. Case sensitive. Must be a text channel. E.G st channel general')
async def set_channel_preference(ctx, channel_name):

    channel = discord.utils.get(ctx.guild.channels, name=channel_name)
    validation = bot_commands.validate_channel_preference(channel, channel_name)

    if validation:
        await ctx.send(validation)
        return
    
    res = db.set_guild_setting(ctx.guild.id, 'CHANNEL_PREFERENCE', channel.id)
    if not res:
        await ctx.send('Something went wrong')
        return

    await ctx.send(f"Success, `{channel_name}` set for member joined updates") 
   
    

bot.run(TOKEN)



