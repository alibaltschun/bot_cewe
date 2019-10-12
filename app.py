from flask import Flask, request, abort , send_from_directory
import os
import flex, db
from decouple import config

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    ImageMessage, FlexSendMessage , CarouselContainer
)



line_bot_api = LineBotApi(config("LINE_CHANNEL_ACCESS_TOKEN",
           default=os.environ.get('LINE_ACCESS_TOKEN')))
    
handler = WebhookHandler(config("LINE_CHANNEL_SECRET",
           default=os.environ.get('LINE_CHANNEL_SECRET')))



app = Flask(__name__, static_url_path='')

VOTE_REGEX = ["vote","voting","voted",
              "rate","rating", "voted","-r"]

STATIC = "/static"
LOCAL_STATIC = "."+STATIC
HTTPS = config("NGROK_HTTP",default=os.environ.get('NGROK_HTTP'))

TEXT_HELP = """# Send image message
- add new data (default)
            
# send text message
- Rating cewe
-- syntax : `kony vote_regex id_cewe score`
-- e.g : kony vote 1 1
-- info : give score 0 for invalid data

- Get unrated cewe by user
-- syntax : `kony get'
-- info : return max 5

# info 
vote_regex : {}
score :
10 : njir gorgeous B.G.T
9 : so beautiful
8 : beautiful
7 : not bad
6 : its ok
5 : underated
4,3,2,1 : evil judge
0 : invalid data
""".format(VOTE_REGEX)
    


def __send_help_message__(event):
    line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=TEXT_HELP))

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
    
    # get total data cewe and save new data with filesname {total_data_cewe + 1.jpg}
    n = len([name for name in os.listdir(LOCAL_STATIC) if os.path.isfile(LOCAL_STATIC+"/"+name)])
    filename = LOCAL_STATIC+"/"+str(n)+".jpg"
    with open(filename, 'wb') as fd:
        for chunk in message_content.iter_content():
            fd.write(chunk)
    
    # reply new data saved
    print("send reply")
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="{} saved ".format(filename)))
    
    
@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text = event.message.text.lower()
    words = text.split()
    
    if words[0] == "kony":
        if words[1] in VOTE_REGEX: # vote
            if words[2].isdigit() and words[3].isdigit():
                # Get user id and username
                profile = line_bot_api.get_profile(event.source.user_id)
                name = profile.display_name.replace(" ","_")
                
                # rate cewe to database
                id_cewe , score = words[2] , words[3]
                db.__rate_cewe__(name,id_cewe,score)
                
                # check image is exist and send flex message
                url_img = HTTPS+STATIC+"/"+str(id_cewe)+".jpg"
                if os.path.isfile(LOCAL_STATIC+"/"+str(id_cewe)+".jpg"):
                    list_voter = db.__get_rated__(id_cewe)
                                                    
                    line_bot_api.reply_message(
                        event.reply_token,
                        FlexSendMessage(alt_text='hello',
                                        contents=flex.flex_rated(str(id_cewe),
                                                                 url_img,list_voter)))
                else:
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text="sorry id cewe does not exist"))
        
        elif words[1] == "get" :   
                       
            # get user id and username
            profile = line_bot_api.get_profile(event.source.user_id)
            name = profile.display_name.replace(" ","_")
            
            # get id cewe that not voted by username
            ids_cewe =db. __get_cewe_unvoted__(name)
            
            print(ids_cewe)
            if ids_cewe[0] != -1:
                flex_messages = []
                if len(ids_cewe) > 5:
                    ids_cewe = ids_cewe[:5]
                    
                for id_cewe in ids_cewe:
                    url_img = HTTPS+STATIC+"/"+str(id_cewe)+".jpg"
                    list_voter = db.__get_rated__(id_cewe)
                    
                    flex_message = flex.flex_rated(str(id_cewe),url_img,list_voter)
                    flex_messages.append(flex_message)
                
                print(type(flex_messages[0]))        
                flex_messages = CarouselContainer(flex_messages)
                flex_messages = FlexSendMessage("list cewe",flex_messages)
                line_bot_api.reply_message(event.reply_token,flex_messages)
                    
            else:
                line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text="you already voted all cewe"))
            
            
        elif text == "kony createtablevoting":
            # create table voting
            db.__create_table__()
            
        elif text == "kony help":
            # send kony help
            __send_help_message__(event)
        
        else: # send kony help if user typo
            __send_help_message__(event)


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=False)