import json
import openai
import edge_tts
import subprocess
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse
from backendApp.middleware import line_verify_2
from backendApp.models import Patient
from lineIntegrations.module.lineVerify import getLineUserUidByToken
from pydub import AudioSegment


# @line_verify_2
# @csrf_exempt
def sendMessageToOpenAi(request, *args, **kwargs):
    if request.method == 'POST':
        patient_id = kwargs.get('patient_id')
        data = json.loads(request.body)

        print(data)
        openai.api_key = api_key

        transcript = "用繁體中文回答" + data.get('transcript', '')

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": transcript}],
            stream=False
        )
        if response and response.choices:
            message = response.choices[0].message
            if message:
                response_text = message.content
                response_role = message.role
            else:
                response_text = "No response generated."
                response_role = "Unknown"
        else:
            response_text = "No response generated."
            response_role = "Unknown"
        return JsonResponse({'response': response_text, 'role': response_role})
    else:
        return JsonResponse({'error': 'Unsupported HTTP method'}, status=405)

async def textToSpeech(request):
    if request.method == 'POST':
        text = "哈摟 我是智伴系統，歡迎與我聊天，也歡迎你們與我進行健康諮詢我將提供你們建議，若是身體不適也可以透過旁邊的按鈕通知給照護者喔！"
        voice = "zh-TW-HsiaoChenNeural"
        communicate = edge_tts.Communicate(text=text, voice=voice)

        audio_path = "static/audio/output2.mp3"  # 指定音频文件的存储路径
        await communicate.save(audio_path)
        
        wav_path = audio_path.replace('mp3','wav')
        lipsync_path = wav_path.replace('wav','json')

        convert_mp3_to_wav(audio_path, wav_path)
        convert_wav_to_lipsyncJson(wav_path, lipsync_path)

        # 之後若是虛擬人跟django運行於不同電腦則須改用外部存取方式
        response_data = {
            "audio": audio_path,
            "lipsync": lipsync_path,
            # animation、facialExpression兩個得靠情緒分析獲取、目前先寫死
            "facialExpression": "smile",
            "animation": "Laughing",
        }    
        return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

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
            return JsonResponse({'success': 'ok', 'user_name':patient.patient_name}, status=200)
        else:
            return JsonResponse({'error': 'token error'}, status=405)

@csrf_exempt
def getVerifyPage(request):
    return render(request, 'mediMate.html')

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
