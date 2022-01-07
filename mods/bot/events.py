import mods.db as db
import logging
import traceback
def is_member_joined(before, after):
    return (not before.channel and after.channel is not None)

def get_channel_to_message(discord, bot, guild_id):
    try:
        channelPreference= db.get_guild_setting(guild_id, 'CHANNEL_PREFERENCE')
        if channelPreference is not None:
            return bot.get_channel(int(channelPreference))
        
        #default to first text channel
        guild = discord.utils.find(lambda g: g.id == guild_id, bot.guilds)
        for channel in guild.channels:
            if str(channel.type) == 'text':
                return bot.get_channel(channel.id)
    
    except Exception as e:
        logging.error(e, exc_info=True)
        return None