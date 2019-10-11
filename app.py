from flask import Flask, request, abort , send_from_directory
import os
import sqlite3
import flex
from decouple import config

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageMessage, FlexSendMessage 
)

app = Flask(__name__, static_url_path='')

HTTPS = config("LINE_CHANNEL_ACCESS_TOKEN",
           default=os.environ.get('LINE_ACCESS_TOKEN'))
STATIC = "/static"

line_bot_api = LineBotApi(
    config("LINE_CHANNEL_ACCESS_TOKEN",
           default=os.environ.get('LINE_ACCESS_TOKEN'))
)
# get LINE_CHANNEL_SECRET from your environment variable
handler = WebhookHandler(
    config("LINE_CHANNEL_SECRET",
           default=os.environ.get('LINE_CHANNEL_SECRET'))
)
    

def create_table():
    conn = sqlite3.connect('cewe.db')
    c = conn.cursor()
    
    c.execute('''CREATE TABLE rating
                 (username text , id_cewe integer, rate interger,
                 UNIQUE(username, id_cewe) ON CONFLICT REPLACE)''')
    
    conn.commit()
    conn.close()
    
def rate_cewe(name,id_cewe,rate):
    conn = sqlite3.connect('cewe.db')
    c = conn.cursor()
    
    c.execute("insert or replace into rating values('{}',{},{})".format(name,id_cewe,rate))
    
    conn.commit()
    conn.close()
    
def get_rated(id_cewe):
    conn = sqlite3.connect('cewe.db')
    c = conn.cursor()
    
    rows = []
    for row in c.execute('''select rate,group_concat(username, ",") from rating
                         where id_cewe={}
                         group by rate'''.format(id_cewe)):
        rows.append(row)
    conn.commit()
    conn.close()
    
    return rows
    
def select_all_rating():
    conn = sqlite3.connect('cewe.db')
    c = conn.cursor()
    
    rows = []
    for row in c.execute('select * from rating'):
        rows.append(row)
        
    conn.close()
    return rows

def get_cewe_unvoted(username):
    conn = sqlite3.connect('cewe.db')
    c = conn.cursor()
    
    rows = []
    for row in c.execute('''select id_cewe from rating
                         where username="{}"'''.format(username)):
        rows.append(row)
    conn.commit()
    conn.close()
    
    rows = [i[0] for i in rows]
    n = len([name for name in os.listdir("."+STATIC) if os.path.isfile("."+STATIC+"/"+name)])
    id_cewe = -1
    for i in range(1,n+1):
        if i not in rows:
            id_cewe = i
            break
    return id_cewe
    


@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('static', path)


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    message_content = line_bot_api.get_message_content(event.message.id)
    
    n = len([name for name in os.listdir(STATIC) if os.path.isfile(STATIC+"/"+name)])
    filename = "./static/"+str(n)+".jpg"
    with open(filename, 'wb') as fd:
        for chunk in message_content.iter_content():
            fd.write(chunk)
    
    print("send reply")
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="{} saved ".format(filename)))
    
@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text = event.message.text.lower()
    
    print(text)    
    words = text.split()
    
    if words[0] == "kony":
        if len(words) == 4:
            if words[1] == "rate" or words[1] == "rating" or words[1] == "vote" or words[1] == "voting":
                if words[2].isdigit() and words[3].isdigit():
                    profile = line_bot_api.get_profile(event.source.user_id)
                    name = profile.display_name.replace(" ","_")
                    
                    id_cewe = words[2]
                    score = words[3]
                    rate_cewe(name,id_cewe,score)
                    url_img = HTTPS+STATIC+"/"+str(id_cewe)+".jpg"
                    
                    if os.path.isfile("."+STATIC+"/"+str(id_cewe)+".jpg"):
                        list_voter = get_rated(id_cewe)
                                                        
                        line_bot_api.reply_message(
                            event.reply_token,
                            FlexSendMessage(alt_text='hello',
                                            contents=flex.flex_rated(str(id_cewe),url_img,list_voter)))
                    else:
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text="sorry id cewe does not exist"))
            elif text == "kony get cewe unvoted" or text == "kony get cewe unrating":
                profile = line_bot_api.get_profile(event.source.user_id)
                name = profile.display_name.replace(" ","_")
                
                id_cewe = get_cewe_unvoted(name)
                print(id_cewe)
                if id_cewe != -1:
                    url_img = HTTPS+STATIC+"/"+str(id_cewe)+".jpg"
                    list_voter = get_rated(id_cewe)
                    
                    line_bot_api.reply_message(
                                    event.reply_token,
                                    FlexSendMessage(alt_text='hello',
                                                    contents=flex.flex_rated(str(id_cewe),url_img,list_voter)))
                else:
                    line_bot_api.reply_message(
                                    event.reply_token,
                                    TextSendMessage(text="you already voted all cewe"))
            
        elif text == "kony createtablevoting":
            create_table()
        elif text == "kony help":
            
            text_help = """add data : send image message
            
rating cewe : 'kony rate id_cewe rating'
e.g -> 'kony rate 1 10'
rating range (0-10) 

get unrated cewe by user : 'kony get cewe unvoted 

info keywords:
rate or rating or vote or voting"""
            
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=text_help))





if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=False)