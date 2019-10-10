from flask import Flask, request, abort , send_from_directory
import os
import sqlite3


from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageMessage
)

app = Flask(__name__, static_url_path='')

HTTPS = "https://7e429605.ngrok.io"
STATIC = "./static"

line_bot_api = LineBotApi('xfPpCZHO/w7j29jpXnBDisR8sKF+MAFMvnHdm7w/99w1MMrQ21WfRlEJIdOIPR5xrHWJL4emyQMYpaTq9P4dOA3npas6p0dHCiSn7n+QTpsgPFr1CTx/qAzV43OAVVkn4Pky5hok0xPb0adLle0ylAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('5c981055d3fc5b13b054b0a0b89b928c')

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
    for row in c.execute('''select * from rating
                         where id_cewe={}'''.format(id_cewe)):
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

r = get_rated(1)
print(select_all_rating())
rate_cewe("b",3,2)

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
    text = event.message.text
        
    words = text.split()
    
    if len(words) > 2:
        if words[1] is int and words[2] is int:
            profile = line_bot_api.get_profile(event.source.user_id)
            name = profile.display_name.replace(" ","_")
            
            if not os.path.exists("./rating/"+name):
                os.makedirs("./rating/"+name)
            
            id_cewe = "./static/"+words[1]+".jpg"
            score = words[2]
            
            reply = "{} voted {} by {}".format(id_cewe,name,score)
            rate_cewe(name,id_cewe,score)
            
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(reply))

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)