import json
import openai
import edge_tts
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse
from backendApp.middleware import line_verify_2
from backendApp.models import Patient
from lineIntegrations.module.lineVerify import getLineUserUidByToken

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
        text = "Hi this is the testHi this is the testHi this is the testHi this is the testHi this is the testHi this is the testHi this is the testHi this is the testHi this is the testHi this is the testHi this is the testHi this is the testHi this is the testHi this is the testHi this is the testHi this is the testHi this is the testHi this is the testHi this is the testHi this is the testHi this is the testHi this is the testHi this is the testHi this is the testHi this is the testHi this is the testHi this is the testHi this is the testHi this is the testHi this is the testHi this is the testHi this is the testHi this is the testHi this is the testHi this is the testHi this is the testHi this is the testHi this is the testHi this is the testHi this is the testHi this is the testHi this is the testHi this is the testHi this is the testHi this is the testHi this is the testHi this is the testHi this is the testHi this is the test"
        voice = 'en-US-GuyNeural'

        # 初始化 TTS 引擎
        communicate = edge_tts.Communicate(text=text, voice=voice)

        audio_path = "audio/output2.mp3"  # 指定音频文件的存储路径
        await communicate.save(audio_path)

    #     response_data = {
    #         "audioBase64": audio_data
    #     }    
    #     return JsonResponse(response_data)
        return JsonResponse({'message': 'Audio processed'})
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