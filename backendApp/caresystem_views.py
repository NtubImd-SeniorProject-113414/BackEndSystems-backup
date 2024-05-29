import os
import uuid
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.db.models.functions import Concat
from backendApp.decorator import group_required
from backendApp.forms import  BedForm, CourseSidesForm, MainCourseForm, PatientForm, PurchaseDetailForm, SupplierForm, UserProfileForm
from backendApp.middleware import login_required
from backendApp.module.sideStock import getSideStockBySidesId
from .models import Bed, CourseSides, MainCourse, Patient, Sides, PurchaseDetail, Supplier

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

    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)
    
    return render(request, 'patient_manager.html', {'page_obj': page_obj})


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
    return render(request, 'add_patient.html', {'form': form})

@group_required('caregiver')
@login_required
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

@group_required('caregiver')
@login_required
def delete_patient(request, patient_id):
    patient = get_object_or_404(Patient, patient_id=patient_id)
    patient.delete()
    messages.success(request, '被照護者已刪除。')
    return redirect('patient_manager')

@group_required('caregiver')
@login_required
def bed_manager(request):
    beds = Bed.objects.all().order_by('bed_number')

    query = request.GET.get('q')
    if query:
        beds = beds.filter(Q(bed_number__icontains=query) | Q(patient__patient_name__icontains=query))

    paginator = Paginator(beds, 10)

    page_number = request.GET.get('page')
    
    page_obj = paginator.get_page(page_number)

    return render(request, 'bed_manager.html', {'page_obj': page_obj})

@group_required('caregiver')
@login_required
def add_bed(request):
    if request.method == 'POST':
        form = BedForm(request.POST)
        if form.is_valid():
            bed_number = form.cleaned_data['bed_number']
            patient = form.cleaned_data['patient']
            if patient:
                existing_bed_with_patient = Bed.objects.filter(patient=patient).first()
                if existing_bed_with_patient:
                    form.add_error('patient', '該病人已被分配床位')
                    return render(request, 'add_bed.html', {'form': form, 'operation': '添加'})
            form.save()
            return redirect('bed_manager')
    else:
        form = BedForm()
    return render(request, 'add_bed.html', {'form': form, 'operation': '添加'})

@group_required('caregiver')
@login_required
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

@group_required('caregiver')
@login_required
def delete_bed(request, bed_id):
    bed = get_object_or_404(Bed, bed_id=bed_id)
    bed.delete()
    return redirect('bed_manager')

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

    return render(request, 'supplier_list.html', {'page_obj': page_obj, 'query': query})

@group_required('caregiver')
@login_required
def add_supplier(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('supplierts')
    else:
        form = SupplierForm()
    return render(request, 'add_supplier.html', {'form': form})

@group_required('caregiver')
@login_required
def edit_supplier(request, supplier_id):
    supplier = get_object_or_404(Supplier, supplier_id=supplier_id)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect('supplierts')
    else:
        form = SupplierForm(instance=supplier)
    return render(request, 'edit_supplier.html', {'form': form})

@group_required('caregiver')
@login_required
def delete_supplier(request, supplier_id):
    supplier = get_object_or_404(Supplier, supplier_id=supplier_id)
    supplier.delete()
    return redirect('supplierts')

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

    return render(request, 'main_course_list.html', {'main_courses': page_obj, 'query': query})

@group_required('caregiver')
@login_required
def add_main_course(request):
    if request.method == 'POST':
        form = MainCourseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('main_course_list')
    else:
        form = MainCourseForm()
    return render(request, 'add_main_course.html', {'form': form})

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
    return render(request, 'edit_main_course.html', {'form': form})

@group_required('caregiver')
@login_required
def delete_main_course(request, course_id):
    course = get_object_or_404(MainCourse, course_id=course_id)
    course.delete()
    return redirect('main_course')

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

@group_required('caregiver')
@login_required
def purchase_detail_delete(request, pk):
    detail = get_object_or_404(PurchaseDetail, pk=pk)
    detail.delete()
    return redirect('purchase_detail')

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

    return render(request, 'main_course_bom_form.html', {
        'form': form,
        'course_sides': course_sides,
        'paginator': paginator,
    })

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
    return render(request, 'course_sides_form.html', {
        'form': form
    })

@group_required('caregiver')
@login_required
def delete_course_sides(request, pk):
    cs = get_object_or_404(CourseSides, pk=pk)
    cs.delete()
    return redirect('bom_settings')

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
    return render(request, 'course_sides_form.html', {'form': form})

@group_required('caregiver')
@login_required
def delete_course_sides(request, pk):
    cs = get_object_or_404(CourseSides, pk=pk)
    cs.delete()
    return redirect('bom_settings')

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

    return render(request, 'inventory_management.html', {
        'inventory_data': page_obj,
        'days': days
    })