import datetime
import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *


line_bot_api = LineBotApi('WPKuz6JHpaA3ezn2yM4rQXacGz4IQBCyEZWAt2qdSzCGrwr/dfscWGauXmr4AKJIuN0Nqhm+/kFfIqz9pvmZ0mCe13sVUAOdgDEnY3wAjol5KU18d5xSq05kTevosHuMWGZ4cfnXdeAN933yV8t2RwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('0f60e5abbb4548dd078f9df4d370582a')

@csrf_exempt
def line_bot_webhook(request):
    if request.method == 'POST':
        body = request.body.decode('utf-8')
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            return HttpResponse(status=400)
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=405)

@csrf_exempt
@handler.add(FollowEvent)
def handle_follow_event(event):
    user_id = event.source.user_id
    #line_bot_api.link_rich_menu_to_user(user_id, )
    welcome_message = "歡迎使用本系統！"
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=welcome_message))

@csrf_exempt
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    message_text = event.message.text
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="開發階段"))