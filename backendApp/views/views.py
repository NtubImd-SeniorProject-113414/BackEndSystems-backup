from django.shortcuts import render, redirect
from backendApp.decorator import group_required
from backendApp.middleware import login_required
import os
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from backendApp.decorator import group_required
from backendApp.forms import  *
from backendApp.middleware import login_required
from backendApp.module.sideStock import getSideStockBySidesId
from backendApp.models import *

#首頁
@group_required('caregiver', 'admin', 'pharmacy')
@login_required
def index(request):
    first_name = request.user.first_name
    last_name = request.user.last_name

    if not first_name and not last_name:
        display_name = request.user.username
    else:
        display_name = f"{first_name} {last_name}"

    context = {'username': display_name}
    return render(request, 'index.html', context)

#個人資料編輯
@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('index') 
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'userManagement/edit_profile.html', {'form': form})

#被照護者管理
@group_required('caregiver')
@login_required
def patient_manager(request):
    query = request.GET.get('search', '')
    
    if query:
        patients = Patient.objects.filter(patient_name__icontains=query)
    else:
        patients = Patient.objects.all()
    
    paginator = Paginator(patients, 10)  
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    # 构造一个包含患者和表单的列表
    patients_with_forms = [
        {
            'patient': patient,
            'form': PatientFormEdit(instance=patient)
        }
        for patient in page_obj
    ]
    
    return render(request, 'patientManagement/patient_manager.html', {
        'page_obj': page_obj,
        'patients_with_forms': patients_with_forms
    })

#新增被照護者
@group_required('caregiver')
@login_required
def add_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '被照護者新增成功。')
            return redirect('patient_manager')
    else:
        form = PatientForm()
    return render(request, 'patientManagement/add_patient.html', {'form': form})

#編輯被照護者
@group_required('caregiver')
@login_required
def edit_patient(request, patient_id):
    patient = get_object_or_404(Patient, patient_id=patient_id)
    if request.method == 'POST':
        form = PatientFormEdit(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, '被照護者資訊更新成功。')
            return redirect('patient_manager')
    else:
        form = PatientFormEdit(instance=patient)
    
    return redirect('patient_manager')

#刪除被照護者
@group_required('caregiver')
@login_required
def delete_patient(request, patient_id):
    patient = get_object_or_404(Patient, patient_id=patient_id)
    patient.delete()
    messages.success(request, '被照護者已刪除。')
    return redirect('patient_manager')

#供應商管理
@group_required('caregiver')
@login_required
def supplier_list(request):
    query = request.GET.get('q')
    if query:
        suppliers = Supplier.objects.filter(supplier_name__icontains=query)
    else:
        suppliers = Supplier.objects.all()

    paginator = Paginator(suppliers, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'supplier/supplier_list.html', {'page_obj': page_obj, 'query': query})

#新增供應商
@group_required('caregiver')
@login_required
def add_supplier(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('suppliers')
    else:
        form = SupplierForm()
    return render(request, 'supplier/add_supplier.html', {'form': form})

#編輯供應商
@group_required('caregiver')
@login_required
def edit_supplier(request, supplier_id):
    supplier = get_object_or_404(Supplier, supplier_id=supplier_id)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect('suppliers')
    else:
        form = SupplierForm(instance=supplier)
    return render(request, 'supplier/edit_supplier.html', {'form': form})

#刪除供應商
@group_required('caregiver')
@login_required
def delete_supplier(request, supplier_id):
    supplier = get_object_or_404(Supplier, supplier_id=supplier_id)
    supplier.delete()
    return redirect('supplierts')


#主餐管理
@group_required('caregiver')
@login_required
def main_course_list(request):
    query = request.GET.get('query', '')

    if query:
        main_courses = MainCourse.objects.filter(course_name__icontains=query)
    else:
        main_courses = MainCourse.objects.all()

    paginator = Paginator(main_courses, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'MealManagement/main_course_list.html', {'main_courses': page_obj, 'query': query})

#新增主餐
@group_required('caregiver')
@login_required
def add_main_course(request):
    if request.method == 'POST':
        form = MainCourseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('main_course')
    else:
        form = MainCourseForm()
    return render(request, 'MealManagement/add_main_course.html', {'form': form})

#編輯主餐
@group_required('caregiver')
@login_required
def edit_main_course(request, course_id):
    course = get_object_or_404(MainCourse, course_id=course_id)
    if request.method == 'POST':
        form = MainCourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            if 'course_image' in request.FILES:
                if course.course_image:
                    old_image_path = course.course_image.path
                    if os.path.isfile(old_image_path):
                        os.remove(old_image_path)
            form.save()
            return redirect('main_course')
    else:
        form = MainCourseForm(instance=course)
    return render(request, 'MealManagement/edit_main_course.html', {'form': form})

#刪除主餐
@group_required('caregiver')
@login_required
def delete_main_course(request, course_id):
    course = get_object_or_404(MainCourse, course_id=course_id)
    course.delete()
    return redirect('main_course')


#進貨管理
@group_required('caregiver')
@login_required
def purchase_detail_list(request):
    query = request.GET.get('query', '')

    if query:
        details = PurchaseDetail.objects.filter(sides__sides_name__icontains=query)
    else:
        details = PurchaseDetail.objects.all()

    paginator = Paginator(details, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'purchase/detail_list.html', {'details': page_obj, 'query': query})

#新增進貨
@group_required('caregiver')
@login_required
def purchase_detail_create(request):
    if request.method == 'POST':
        form = PurchaseDetailForm(request.POST)
        if form.is_valid():
            new_detail = form.save()
            return redirect('purchase_detail')
    else:
        form = PurchaseDetailForm()
    return render(request, 'purchase/detail_form.html', {'form': form})

#編輯進貨
@group_required('caregiver')
@login_required
def purchase_detail_update(request, pk):
    detail = get_object_or_404(PurchaseDetail, pk=pk)
    initial_quantity = detail.purchase_quantity
    if request.method == 'POST':
        form = PurchaseDetailForm(request.POST, instance=detail)
        if form.is_valid():
            updated_detail = form.save()
            return redirect('purchase_detail')
    else:
        form = PurchaseDetailForm(instance=detail)
    return render(request, 'purchase/detail_form.html', {'form': form})

#刪除進貨
@group_required('caregiver')
@login_required
def purchase_detail_delete(request, pk):
    detail = get_object_or_404(PurchaseDetail, pk=pk)
    detail.delete()
    return redirect('purchase_detail')


#主餐bom表管理(管理主餐內的配菜)
@group_required('caregiver')
@login_required
def main_course_bom_settings(request):
    if request.method == 'POST':
        form = CourseSidesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bom_settings')
    else:
        form = CourseSidesForm()

    course_sides_list = CourseSides.objects.select_related('course', 'sides').all()
    paginator = Paginator(course_sides_list, 10)
    page_number = request.GET.get('page')
    course_sides = paginator.get_page(page_number)

    return render(request, 'MealManagement/main_course_bom_form.html', {
        'form': form,
        'course_sides': course_sides,
        'paginator': paginator,
    })

#編輯主餐bom表(調整主餐中的配菜與數量)
@group_required('caregiver')
@login_required
def edit_course_sides(request, pk):
    cs = get_object_or_404(CourseSides, pk=pk)
    if request.method == 'POST':
        form = CourseSidesForm(request.POST, instance=cs)
        if form.is_valid():
            form.save()
            return redirect('bom_settings')
    else:
        form = CourseSidesForm(instance=cs)
    return render(request, 'MealManagement/course_sides_form.html', {
        'form': form
    })

#刪除主餐中的配菜
@group_required('caregiver')
@login_required
def delete_course_sides(request, pk):
    cs = get_object_or_404(CourseSides, pk=pk)
    cs.delete()
    return redirect('bom_settings')


#配菜存貨管理
@group_required('caregiver')
@login_required
def inventory_management(request):
    total_patients = Patient.objects.count()
    
    days = int(request.GET.get('days', 7))  

    sides = Sides.objects.all()
    
    inventory_data = []
    for side in sides:
        total_needed = 0
        SideStock = getSideStockBySidesId(side.sides_id)
        SideStock = SideStock if SideStock >= 0 else 0
        total_needed = SideStock * total_patients * days
        inventory_data.append({
            'sides_name': side.sides_name,
            'current_stock': SideStock,
            'minimum_required': total_needed,
        })

    paginator = Paginator(inventory_data, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'MealManagement/inventory_management.html', {
        'inventory_data': page_obj,
        'days': days
    })

#取得配菜數量
def get_sides_unit(request, sides_id):
    sides = Sides.objects.filter(sides_id=sides_id).first()
    if sides:
        return JsonResponse({'sides_unit': sides.sides_unit})
    else:
        return JsonResponse({'sides_unit': ''})

#新增配菜
@group_required('caregiver')
@login_required
def sides_create(request):
    if request.method == 'POST':
        form = AddSides(request.POST)
        if form.is_valid():
            new_detail = form.save()
            return redirect('bom_settings')
    else:
        form = AddSides()
    return render(request, 'MealManagement/add_sides.html', {'form': form})