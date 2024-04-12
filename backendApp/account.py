from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from .forms import CustomUserCreationForm 
from backendApp.decorator import group_required
from backendApp.middleware import login_required

def is_superuser(user):
    return user.is_authenticated and user.is_superuser


@user_passes_test(is_superuser, login_url='/login', redirect_field_name=None)
@login_required
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '註冊成功！')
            return redirect('login')  
    else:
        form = CustomUserCreationForm()
    return render(request, 'creat_account.html', {'form': form})