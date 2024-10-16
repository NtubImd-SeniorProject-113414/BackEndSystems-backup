import json
import openai
import edge_tts
import subprocess
import base64
import asyncio

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from backendApp.middleware import line_verify_2
from backendApp.models import ChatLogs, Patient, MedicineDemand, MedicineDemandState
from lineIntegrations.module.lineVerify import getLineUserUidByToken
from pydub import AudioSegment
from asgiref.sync import sync_to_async
from django.utils import timezone

charactors = ['/male1', '/male2', '/female1', '/female2']
voice_param = ["zh-TW-HsiaoChenNeural", "", "", ""]
openai.api_key = ''

@csrf_exempt
def setSessionByToken(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        access_token = data.get('token', '')
        lineUid = getLineUserUidByToken(access_token)
        patient_id = Patient.getpatientIdByLineUid(lineUid)
        patient = Patient.objects.filter(patient_id=patient_id).first()
        if patient_id != None:
            request.session['line_access_token'] = access_token
            return JsonResponse({'success': 'ok', 'userName':patient.patient_name}, status=200)
        else:
            return JsonResponse({'error': 'token error'}, status=405)

@csrf_exempt
def getVerifyPage(request):
    return render(request, 'mediMate.html')

# @line_verify_2
# @csrf_exempt
async def sendMessageToOpenAi(request, *args, **kwargs):
    if request.method == 'POST':
        data = json.loads(request.body)
        patient_name = data['userName']
        transcript = data['transcript']
    
        chat_logs = await get_today_chat_logs(patient_name)
        
        history = [
            {"role": "user", "content": log.patient_message}
            for log in chat_logs
        ] + [
            {"role": "assistant", "content": log.response_message}
            for log in chat_logs
        ]
        
        prompt = f"""
            你是一個大系統中重要的虛擬人，專門為長照中心的被照護者提供服務。你的角色是幫助緩解被照護者在床上或感到無聊時的孤單感，可以和他們進行聊天和互動。當被照護者想與你交談時，你需要以友善和耐心的方式回應他們的問題，並根據以下指導提供幫助：
            1. **健康諮詢**：根據常識和一般健康信息提供建議，但避免具體的醫療診斷或治療建議。
            2. **娛樂互動**：提供輕鬆、有趣的聊天，幫助緩解被照護者的無聊感，讓他們感到愉快和放鬆。
            3. **生活建議**：在日常生活、運動、飲食等方面給予實用的建議，讓被照護者感到受到照顧。
            4. **不適情況處理**：系統有一個專門的功能，當被照護者感到不舒服時，可以點擊特定按鈕，彈出一個窗口填寫具體的不舒服訊息。你需要提醒被照護者，如果他們感到不適，可以使用這個功能來報告他們的情況。

            請保持語氣溫暖、耐心，並且希望你講話像是人一樣不要過多的贅字遣詞，回答時盡量簡單，並根據被照護者的需求調整你的回應。如果你發現他們提到了不舒服，可以提醒他們使用畫面中右邊第二個醫生按鈕來回報醫護人員。
            
            並且目前正與 {patient_name} 對話中
        """
        history.append({"role": "user", "content": transcript})
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": prompt}] + history,
            stream=False
        )

        if response and response.choices:
            response_text = response.choices[0].message['content']
            
            await save_chat_log(patient_name, transcript, response_text)
            
            audio_path = "static/audio/chat.mp3"
            voice_param = "zh-CN-XiaoxiaoNeural"
            audioWithJsonData = await generate_video_lipsync_convert_file(response_text, audio_path, voice_param)

            data = {
                'text': response_text,
                "audio": audioWithJsonData['audioBase64'],
                "lipsync": audioWithJsonData['lipsync_data'],
                "facialExpression": "smile",
                "animation": "Idle",
            }
            
            return JsonResponse(data)

        else:
            return JsonResponse({'error': '未知錯誤'}, status=405)
    else:
        return JsonResponse({'error': 'Unsupported HTTP method'}, status=405)
    

@csrf_exempt
def helloUserInfoAndVideo(request, *args, **kwargs):
    if request.method == 'POST':
        data = json.loads(request.body)
        patient_name = data['userName']
        text = f"{patient_name}您好！請問今天需要甚麼幫助呢！"
        audio_path = "static/audio/hellouser.mp3"
        voice_param = "zh-CN-XiaoxiaoNeural"

        audioWithJsonData = asyncio.run(generate_video_lipsync_convert_file(text, audio_path, voice_param))
        
        data = {
            'text': text,
            'role': "assistant",
            "audio": audioWithJsonData['audioBase64'],
            "lipsync": audioWithJsonData['lipsync_data'],
            "facialExpression": "smile",
            "animation": "Waving",
        }

        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Unsupported HTTP method'}, status=405)
    
@csrf_exempt
def sendUncomfortableMessage(request, *args, **kwargs):
    if request.method == 'POST':
        data = json.loads(request.body)
        patient_name = data['userName']
        transcript = data['transcript']
        
        text = f"已收到{patient_name}您的通知！我們已經通知了護理人員，稍後會有專業人員前來了解您的狀況。"
        audio_path = "static/audio/uncomfortableMessage.mp3"
        voice_param = "zh-CN-XiaoxiaoNeural"

        audioWithJsonData = asyncio.run(generate_video_lipsync_convert_file(text, audio_path, voice_param))
        
        patient = Patient.objects.get(patient_name=patient_name)
        medicine_demand_state = MedicineDemandState.objects.get(medicineDemandState_code=1)

        medicine_demand = MedicineDemand.objects.create(
            patient=patient,
            patient_demand=transcript,
            medicineDemandState=medicine_demand_state,
            created_time=timezone.now()
        )
        medicine_demand.save()

    
        data = {
            'text': text,
            'role': "assistant",
            "audio": audioWithJsonData['audioBase64'],
            "lipsync": audioWithJsonData['lipsync_data'],
            "facialExpression": "smile",
            "animation": "Idle",
        }

        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Unsupported HTTP method'}, status=405)

# 異步函數來處理 lipsync 和音訊生成
async def generate_video_lipsync_convert_file(text, audio_path, voice_param):
    communicate = edge_tts.Communicate(text=text, voice=voice_param)
    await communicate.save(audio_path)

    wav_path = audio_path.replace('mp3', 'wav')
    lipsync_path = wav_path.replace('wav', 'json')

    convert_mp3_to_wav(audio_path, wav_path)
    convert_wav_to_lipsyncJson(wav_path, lipsync_path)
    
    audioBase64 = convert_audio_to_base64(audio_path)
    lipsync_data = read_json_file(lipsync_path)
    
    audio_with_json = {
        'audioBase64': audioBase64,
        'lipsync_data': lipsync_data,
    }
    
    return audio_with_json

def convert_mp3_to_wav(input_mp3, output_wav):
    try:
        audio = AudioSegment.from_mp3(input_mp3)
        audio.export(output_wav, format="wav")    
    except:
        print('請安裝"語音轉檔套件"，並設定環境變數 - ffmpeg (參考 readme)')
    
def convert_wav_to_lipsyncJson(input_wav, output_json):
    # 請先自行安裝好環境變數 (參考 readme)
    try:
        command = [
            'rhubarb',
            '-o', output_json,
            input_wav,
            '-r', 'phonetic',
            '-f', 'json'
        ]
        subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except:
        print('請安裝"wav轉嘴型json檔案套件"，並設定環境變數 - rhubarb lipsync (參考 readme)')

def convert_audio_to_base64(filepath):
    with open(filepath, "rb") as audio_file:
        audio_data = audio_file.read()
        audio_base64 = base64.b64encode(audio_data).decode('utf-8')
    return audio_base64

def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

@sync_to_async
def save_chat_log(patient_name, patient_message, response_message):
    try:
        patient = Patient.objects.get(patient_name=patient_name)

        # 創建新的對話紀錄
        chat_log = ChatLogs.objects.create(
            patient=patient,
            patient_message=patient_message,
            response_message=response_message,
        )
        chat_log.save()

    except Patient.DoesNotExist:
        print("找不到對應的病人資料")
    except Patient.MultipleObjectsReturned:
        print("多個病人擁有相同的名字，請確認唯一性")
    except Exception as e:
        print(f"保存對話紀錄時發生錯誤: {e}")
        

async def get_today_chat_logs(patient_name):
    try:
        patient = await sync_to_async(Patient.objects.get)(patient_name=patient_name)
        today = timezone.now().date()

        chat_logs = await sync_to_async(list)(
            ChatLogs.objects.filter(
                patient=patient,
                created_time__date=today
            ).order_by('created_time')
        )

        return chat_logs

    except Patient.DoesNotExist:
        print("找不到對應的病人資料")
        return []

def get_voice_param_by_location(location):
    for i in range(len(charactors)):
        if charactors[i] == location:
            return voice_param[i]