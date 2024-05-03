from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse

@csrf_exempt
def getWebPage(request):
    print(request.method)
    if request.method == 'GET':
        return render(request, 'none.html')
    return HttpResponse("Unsupported HTTP method", status=405)