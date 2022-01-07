def validate_channel_preference(channel, channel_name):

    if channel is None:
        return f"Cannot find channel `{channel_name}`. Channels are case sensitive"
    if str(channel.type) != "text":
        return f"`{channel_name}` is not a text channel. Channels are case sensitive"
    
    return ''