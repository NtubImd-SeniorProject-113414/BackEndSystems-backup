import json
import openai
import edge_tts
import subprocess
import base64
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse
from backendApp.middleware import line_verify_2
from backendApp.models import Patient
from lineIntegrations.module.lineVerify import getLineUserUidByToken
from pydub import AudioSegment

voice_param = "zh-TW-HsiaoChenNeural"

# @line_verify_2
# @csrf_exempt
async def sendMessageToOpenAi(request, *args, **kwargs):
    if request.method == 'POST':
        # patient_id = kwargs.get('patient_id')
        data = json.loads(request.body)

        openai.api_key = 'test'

        transcript = "用繁體中文回答：" + data.get('transcript', '')
    
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": transcript}],
            stream=False
        )
        if response and response.choices:
            message = response.choices[0].message
            if message:
                # response_text = message.content
                # response_role = message.role
                response_text = "當然可以，請問你需要什麼幫助呢？我會盡力幫你解決問題。"
                response_role = "assistant"
                audio_path = "static/audio/output2.mp3"
                communicate = edge_tts.Communicate(text=response_text, voice=voice_param)
                await communicate.save(audio_path)
                
                wav_path = audio_path.replace('mp3','wav')
                lipsync_path = wav_path.replace('wav','json')
                
                convert_mp3_to_wav(audio_path, wav_path)
                convert_wav_to_lipsyncJson(wav_path, lipsync_path)
        if response_text:
            audioBase64 = convert_audio_to_base64(audio_path);
            lipsync_data = read_json_file(lipsync_path)
            data = {
                'text': response_text,
                'role': response_role,
                "audio":  audioBase64,
                "lipsync": lipsync_data,
                "facialExpression": "smile",
                "animation": "Laughing",
            }
            return JsonResponse(data)
        else:
            return JsonResponse({'error': '未知錯誤'}, status=405)
    else:
        return JsonResponse({'error': 'Unsupported HTTP method'}, status=405)

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

def convert_audio_to_base64(filepath):
    with open(filepath, "rb") as audio_file:
        audio_data = audio_file.read()
        audio_base64 = base64.b64encode(audio_data).decode('utf-8')
    return audio_base64

def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)