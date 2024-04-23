from django.contrib import messages
from django.http import HttpResponseForbidden, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from jsonschema import ValidationError
from django.db.models import F
from backendApp.decorator import group_required
from backendApp.forms import PatientForm, UserProfileForm
from backendApp.middleware import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, Value
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Patient
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User,Group
from django.db.models.functions import Concat


@group_required('admin')
@login_required
def caregiver_manager(request):
    query = request.GET.get('search', '').strip()
    if query:
        caregivers = User.objects.filter(groups__name='caregiver').annotate(
            full_name=Concat('first_name','last_name')
        ).filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(full_name__icontains=query)  
        )
    else:
        caregivers = User.objects.filter(groups__name='caregiver')

    if request.method == 'POST':
        if 'delete' in request.POST:
            user_id = request.POST.get('delete')
            User.objects.filter(id=user_id).delete()
        elif 'edit' in request.POST:
            user_id = request.POST.get('edit')
            caregiver_to_edit = get_object_or_404(User, id=user_id)
            form = UserProfileForm(request.POST, instance=caregiver_to_edit)
            if form.is_valid():
                form.save()
                return redirect('caregiver_manager')

    return render(request, 'caregiver_manager.html', {'caregivers': caregivers})

@login_required
@group_required('admin')
def edit_caregiver(request, caregiver_id):
    caregiver_to_edit = get_object_or_404(User, id=caregiver_id)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=caregiver_to_edit)
        if form.is_valid():
            form.save()
            return redirect('caregiver_manager')
    else:
        form = UserProfileForm(instance=caregiver_to_edit)
    
    return render(request, 'caregiver_edit.html', {'form': form, 'caregiver_id': caregiver_id})


def patient_manager(request):
    query = request.GET.get('search', '')
    
    if query:
        patients = Patient.objects.filter(patient_name__icontains=query)
    else:
        patients = Patient.objects.all()
    
    # 分頁設置，每頁顯示 10 筆資料
    paginator = Paginator(patients, 10)  # 每頁顯示 10 筆資料
    page_number = request.GET.get('page', 1)

    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        # 如果頁碼不是一個整數，返回第一頁。
        page_obj = paginator.get_page(1)
    except EmptyPage:
        # 如果頁碼太大，沒有那麼多頁，返回最後一頁。
        page_obj = paginator.get_page(paginator.num_pages)
    
    return render(request, 'patient_manager.html', {'page_obj': page_obj})

def add_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '被照護者新增成功。')
            return redirect('patient_manager')
    else:
        form = PatientForm()
    return render(request, 'add_patient.html', {'form': form})

def edit_patient(request, patient_id):
    patient = get_object_or_404(Patient, patient_id=patient_id)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, '被照護者資訊更新成功。')
            return redirect('patient_manager')
    else:
        form = PatientForm(instance=patient)
    return render(request, 'edit_patient.html', {'form': form, 'patient': patient})

def delete_patient(request, patient_id):
    patient = get_object_or_404(Patient, patient_id=patient_id)
    patient.delete()
    messages.success(request, '被照護者已刪除。')
    return redirect('patient_manager')