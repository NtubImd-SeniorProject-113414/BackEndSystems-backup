from django import forms
from django.contrib import messages
from django.http import HttpResponseForbidden, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from jsonschema import ValidationError
from django.db.models import F
from backendApp.decorator import group_required
from backendApp.middleware import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import models
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User,Group

@group_required('admin')
@login_required
def  caregiver_manager(request):
    caregivers = User.objects.filter(groups__name='caregiver')
        # 如果是 POST 請求，處理修改或刪除
    if request.method == 'POST':
        if 'delete' in request.POST:
            user_id = request.POST.get('delete')
            User.objects.filter(id=user_id).delete()
        elif 'edit' in request.POST:
            user_id = request.POST.get('edit')
            # 在這裡加入修改的邏輯
            pass
    
    return render(request, 'caregiver_manager.html', {'caregivers': caregivers})