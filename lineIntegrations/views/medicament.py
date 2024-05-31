import json
import openai
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse
from backendApp.middleware import line_verify

@csrf_exempt
def sendMessageToOpenAi(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        transcript = data.get('transcript', '')
        client = None
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": transcript}],
            stream=False,
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

@csrf_exempt
def getVerifyPage(request):
    return render(request, 'mediMate.html')