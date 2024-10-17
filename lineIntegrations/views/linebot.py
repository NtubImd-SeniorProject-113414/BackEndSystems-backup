from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
from backendApp.models import *
from decouple import config


# Line Bot API 的 Token 和 Secret
line_bot_api = LineBotApi(config('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(config('LINE_CHANNEL_SECRET'))

# richmenu tokens
registerMenuToken = config('REGISTER_MENU_TOKEN')
infoMenuToken = config('INFO_MENU_TOKEN')
serviceMenuToken = config('SERVICE_MENU_TOKEN')

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
    if Patient.getpatientIdByLineUid(user_id) != None:
        line_bot_api.link_rich_menu_to_user(user_id, infoMenuToken)
    else:
        line_bot_api.link_rich_menu_to_user(user_id, registerMenuToken)
        welcome_message = "歡迎使用本系統！請先進行註冊"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=welcome_message))

@csrf_exempt
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    message_text = event.message.text
    if Patient.getpatientIdByLineUid(user_id) != None:
        if message_text == "@服務選單":
            line_bot_api.link_rich_menu_to_user(user_id, serviceMenuToken)
        elif message_text == "@資訊查看" or message_text == "@完成註冊":
            line_bot_api.link_rich_menu_to_user(user_id, infoMenuToken)
    else:
        line_bot_api.link_rich_menu_to_user(user_id, registerMenuToken)
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="尚未註冊"))

