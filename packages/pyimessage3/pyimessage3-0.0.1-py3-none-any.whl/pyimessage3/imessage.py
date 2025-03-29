import sqlite3
import datetime
import os
import tempfile

def get_chat_mapping(db_location):
    conn = sqlite3.connect(db_location)
    cursor = conn.cursor()

    cursor.execute("SELECT room_name, display_name FROM chat")
    result_set = cursor.fetchall()

    mapping = {room_name: display_name for room_name, display_name in result_set}

    conn.close()

    return mapping
def read_messages(db_location, n=10,  human_readable_date=True,read_group=False):
    conn = sqlite3.connect(db_location)
    cursor = conn.cursor()
    query = """
    SELECT message.ROWID, message.date, message.text, message.attributedBody, handle.id, message.cache_roomnames
    FROM message
    LEFT JOIN handle ON message.handle_id = handle.ROWID 
    where message.is_from_me = 0 
    AND (message.text IS NOT NULL OR message.attributedBody IS NOT NULL)
    AND handle.id IS NOT NULL
    """
    if read_group!=True:
        query += "AND message.cache_roomnames IS NULL"
    if n is not None:
        query += f" ORDER BY message.date DESC LIMIT {n}"
    results = cursor.execute(query).fetchall()
    messages = []
    for result in results:
        rowid, date, text, attributed_body, handle_id, cache_roomname = result
        phone_number = handle_id
        if text is not None:
            body = text
        elif attributed_body != None:
            attributed_body = attributed_body.decode('utf-8', errors='replace')
            if "NSNumber" in str(attributed_body):
                attributed_body = str(attributed_body).split("NSNumber")[0]
                if "NSString" in attributed_body:
                    attributed_body = str(attributed_body).split("NSString")[1]
                    if "NSDictionary" in attributed_body:
                        attributed_body = str(attributed_body).split("NSDictionary")[0]
                        attributed_body = attributed_body[6:-12]
                        body = attributed_body
        if human_readable_date:
            date_string = '2001-01-01'
            mod_date = datetime.datetime.strptime(date_string, '%Y-%m-%d')
            unix_timestamp = int(mod_date.timestamp())*1000000000
            new_date = int((date+unix_timestamp)/1000000000)
            date = datetime.datetime.fromtimestamp(new_date).strftime("%Y-%m-%d %H:%M:%S")
        mapping = get_chat_mapping(db_location)
        try:
            mapped_name = mapping[cache_roomname]
        except:
            mapped_name = None
        messages.append(
            {"rowid": rowid, "date": date, "body": body, "phone_number": phone_number,
             "cache_roomname": cache_roomname, 'group_chat_name' : mapped_name})
    conn.close()
    return messages



def send_imessage(receiver,msg,group=False):
    with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8', suffix='.txt') as temp_file:
        temp_filename = temp_file.name
        temp_file.write(msg)
    try:
        if group:
            apple_script = f"""
                tell application "Messages"
                    send (read (POSIX file "{temp_filename}") as «class utf8») to chat "{receiver}"
                end tell
            """
        else:
            apple_script = f"""
                tell application "Messages"
                    set targetBuddy to buddy "{receiver}" of (1st service whose service type = iMessage)
                    send (read (POSIX file "{temp_filename}") as «class utf8») to targetBuddy
                end tell
            """
        os.system(f'osascript -e \'{apple_script}\'')
    finally:
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
