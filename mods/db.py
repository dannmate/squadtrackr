import os
import logging
import traceback

from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(url, key)

def has_data(data):
    return len(data[0]) > 0
    
def add_member_join_event(guild_id, member_id, member_display_name):
    data = supabase.table('MEMBER_JOIN_EVENT').insert({'guild_id': guild_id, 'member_id': member_id, 'member_display_name': member_display_name}).execute()
    check_db_call(data)

def check_db_call(data):
    if not has_data(data):
        logging.error('No data returned from db call')
        return False
    if type(data[0]) is not list and 'message' in data[0] and 'code' in data[0]:
        logging.error("Database exception: %s", data[0].get('message'))
        return False
    return True


    


