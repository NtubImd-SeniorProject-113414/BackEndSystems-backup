from django.shortcuts import render
from backendApp.models import Patient
from lineIntegrations.module.lineVerify import getLineUserUidByToken, getLineTokenByRequest

class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response
    
def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, 'deny.html')
        
        return view_func(request, *args, **kwargs)
    return wrapper

def line_verify(view_func):
    def wrapper(request, *args, **kwargs):
        getLineTokenByRequest(request)
        access_token = request.session.get('line_access_token')
        lineUid = getLineUserUidByToken(access_token)
        patient_id = Patient.getpatientIdByLineUid(lineUid)
        if patient_id == None:
            return render(request, 'deny.html')
        kwargs['patient_id'] = patient_id
        return view_func(request, *args, **kwargs)
    return wrapper