import os
import logging
import traceback

from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(url, key)

    
def add_member_join_event(guild_id, member_id, member_display_name):
    data = supabase.table('MEMBER_JOIN_EVENT').insert({'guild_id': guild_id, 'member_id': member_id, 'member_display_name': member_display_name}).execute()
    check_db_call(data)

def check_db_call(data):
    if type(data[0]) is not list and 'message' in data[0] and 'code' in data[0]:
        logging.error("Database exception: %s", data[0].get('message'))
        return False
    return True

def get_guild_setting(guild_id, key):
    data = supabase.table("GUILD_SETTINGS").select("*").eq('guild_id', guild_id).eq('key',key).execute()
    if not check_db_call(data) or len(data[0]) == 0:
        return None
    return data[0][0].get('value')    

def set_guild_setting(guild_id, key, value):
    if get_guild_setting(guild_id, key) is None:
        data = supabase.table('GUILD_SETTINGS').insert({'guild_id': guild_id, 'key': key, 'value': value}).execute()
        return check_db_call(data)
             
    data = supabase.table('GUILD_SETTINGS').update({ 'value': value }).eq('guild_id', guild_id).eq('key',key).execute()
    return check_db_call(data)
    


