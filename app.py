from flask import Flask, request, abort , send_from_directory
import os
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageMessage ,ImageSendMessage
)

app = Flask(__name__, static_url_path='')

HTTPS = "https://7e429605.ngrok.io"
STATIC = "./static"

line_bot_api = LineBotApi('2IOn+t2c+RRzIN7mkVbNd5cq0Sl8F6Q5FqhbisyrR1f1fv3BZgFDeXrPek8CYVV+mHrMKZ/z+TpDekpmPRcJ+JhCR7Sz9TaA0Iah9tSVpxRYr9OXv/pCUBSXU/mGOnMWRCkpPl5BkvDXw6XRctUVZQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('68c2a96b847785ad05aa8e42f4e9a17c')

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



if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)