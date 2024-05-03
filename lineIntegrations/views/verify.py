from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse
from backendApp.models import Patient

@csrf_exempt
def getWebPage(request):
    print(request.method)
    if request.method == 'GET':
        return render(request, 'verify.html')
    elif request.method == 'POST':
        name = request.POST.get('name')
        idCard = request.POST.get('idCard')
        phone = request.POST.get('phone')
        lineUid = request.POST.get('lineUid')
        req = Patient.createLineAccount(name, idCard, phone, lineUid)
        return render(request, 'verify.html', req)
    return HttpResponse("Unsupported HTTP method", status=405)
