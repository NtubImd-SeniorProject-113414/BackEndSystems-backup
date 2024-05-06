from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from backendApp.models import Notify
from backendApp.middleware import line_verify


@csrf_exempt
def getWebPage(request):
    return render(request, 'order/menu.html')

def getPatientNotifyList(request):
    return JsonResponse({'message': 'test'}, status=201)
