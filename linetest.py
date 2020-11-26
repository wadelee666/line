from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('589QAvkXTKz5tSWWCocKD7c0zOyqSCheUbaEnfREhNvu4JFjBZfnd0y3zf/FmIlZZLElLbvNh+ATx/9pG/eccefKN/o5NMMuKZUrW7FOSgy0Y+/QRshd5d6p2nJg0Bj13uOKtV/Tw64qNB5Qw8JFVgdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('e16a071bfc02c57783d2153c62fb855d')

# 監聽所有來自 /callback 的 Post Request
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
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token, message)

@handler.add(BeaconEvent)
def handle_beacon_event(event):
	if event.beacon.hwid == '01458a1757':
		msg = "以連接上藍芽"
	line_bot_api.reply_message(
	event.reply_message,
	TextMessage(text = msg)
	)
	
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
