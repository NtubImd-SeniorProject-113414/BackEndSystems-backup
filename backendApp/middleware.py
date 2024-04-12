from django.shortcuts import render


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