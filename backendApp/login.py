from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from backendApp.middleware import login_required
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if hasattr(user, 'last_login') and (timezone.now() - user.last_login) < timedelta(seconds=20):
                return render(request, 'login.html', {'error': '登入嘗試過於頻繁，請稍後再試。'})
            request.session.flush()
            login(request, user)
            user.fail_count = 0
            user.save()
            return redirect('index')
        else:
            try:
                user = User.objects.get(username=username)
                if hasattr(user, 'fail_count'):
                    user.fail_count += 1
                else:
                    user.fail_count = 1
                user.save()
            except User.DoesNotExist:
                pass
            return render(request, 'login.html', {'error': '帳號或密碼錯誤'})
    else:
        return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')