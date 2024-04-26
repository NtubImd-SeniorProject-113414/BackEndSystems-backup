from django.contrib import messages
from django.http import HttpResponseForbidden, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from jsonschema import ValidationError
from django.db.models import F
from backendApp.decorator import group_required
from backendApp.forms import BedForm, PatientForm, UserProfileForm
from backendApp.middleware import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, Value
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Bed, Patient
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


def bed_manager(request):
    # 获取所有床位对象，并按照床位编号排序
    beds = Bed.objects.all().order_by('bed_number')

    # 获取搜索框中用户输入的搜索条件
    query = request.GET.get('q')
    if query:
        # 如果有搜索条件，则使用 Q 对象构造一个搜索查询，包括床位编号和病人姓名
        beds = beds.filter(Q(bed_number__icontains=query) | Q(patient__patient_name__icontains=query))

    # 创建一个 Paginator 对象，每页显示 10 条记录
    paginator = Paginator(beds, 10)

    # 获取请求的页数，默认为第一页
    page_number = request.GET.get('page')
    
    # 根据请求的页数获取对应的数据
    page_obj = paginator.get_page(page_number)

    return render(request, 'bed_manager.html', {'page_obj': page_obj})

def add_bed(request):
    if request.method == 'POST':
        form = BedForm(request.POST)
        if form.is_valid():
            bed_number = form.cleaned_data['bed_number']
            patient = form.cleaned_data['patient']
            
            if patient:
                existing_bed_with_patient = Bed.objects.filter(patient=patient).first()
                if existing_bed_with_patient:
                    form.add_error('patient', '该病人已被分配床位。')
                    return render(request, 'add_bed.html', {'form': form})
            
            form.save()
            return redirect('bed_manager')
    else:
        form = BedForm() 
    return render(request, 'add_bed.html', {'form': form})

def edit_bed(request, bed_id):
    bed = get_object_or_404(Bed, bed_id=bed_id)
    if request.method == 'POST':
        form = BedForm(request.POST, instance=bed)
        if form.is_valid():
            form.save()
            return redirect('bed_manager')
    else:
        form = BedForm(instance=bed)
    return render(request, 'edit_bed.html', {'form': form})


def delete_bed(request, bed_id):
    bed = get_object_or_404(Bed, bed_id=bed_id)
    bed.delete()
    return redirect('bed_manager')