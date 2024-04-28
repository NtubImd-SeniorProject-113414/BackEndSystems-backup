import os
from django.contrib import messages
from django.http import HttpResponseForbidden, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from jsonschema import ValidationError
from django.db.models import F
from backendApp.decorator import group_required
from backendApp.forms import  BedForm, CourseSidesForm, MainCourseForm, PatientForm, StockingDetailForm, StockingForm, SupplierForm, UserProfileForm
from backendApp.middleware import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, Value
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Bed, CourseSides, MainCourse, Patient, Sides, Stocking, StockingDetail, Supplier
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

@group_required('admin','caregiver')
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


@group_required('admin','caregiver')
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

@group_required('admin','caregiver')
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

@group_required('admin','caregiver')
@login_required
def delete_patient(request, patient_id):
    patient = get_object_or_404(Patient, patient_id=patient_id)
    patient.delete()
    messages.success(request, '被照護者已刪除。')
    return redirect('patient_manager')

@group_required('admin','caregiver')
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

@group_required('admin','caregiver')
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

@group_required('admin','caregiver')
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

@group_required('admin','caregiver')
@login_required
def delete_bed(request, bed_id):
    bed = get_object_or_404(Bed, bed_id=bed_id)
    bed.delete()
    return redirect('bed_manager')

@group_required('admin')
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

@group_required('admin')
@login_required
def add_supplier(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('supplier_list')
    else:
        form = SupplierForm()
    return render(request, 'add_supplier.html', {'form': form})

@group_required('admin')
@login_required
def edit_supplier(request, supplier_id):
    supplier = get_object_or_404(Supplier, supplier_id=supplier_id)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect('supplier_list')
    else:
        form = SupplierForm(instance=supplier)
    return render(request, 'edit_supplier.html', {'form': form})

@group_required('admin')
@login_required
def delete_supplier(request, supplier_id):
    supplier = get_object_or_404(Supplier, supplier_id=supplier_id)
    supplier.delete()
    return redirect('supplier_list')

@group_required('admin')
@login_required
def main_course_list(request):
    query = request.GET.get('query', '')

    if query:
        main_courses = MainCourse.objects.filter(course_name__icontains=query)
    else:
        main_courses = MainCourse.objects.all()

    paginator = Paginator(main_courses, 10)  # 每页显示10条记录
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'main_course_list.html', {'main_courses': page_obj, 'query': query})

@group_required('admin')
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

@group_required('admin')
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
            return redirect('main_course_list')
    else:
        form = MainCourseForm(instance=course)
    return render(request, 'edit_main_course.html', {'form': form})

@group_required('admin')
@login_required
def delete_main_course(request, course_id):
    course = get_object_or_404(MainCourse, course_id=course_id)
    course.delete()
    return redirect('main_course_list')

@group_required('admin')
@login_required
def stocking_detail_list(request):
    query = request.GET.get('query', '')

    if query:
        details = StockingDetail.objects.filter(sides__sides_name__icontains=query)
    else:
        details = StockingDetail.objects.all()

    paginator = Paginator(details, 10)  # 每页显示10条记录
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'stocking_detail_list.html', {'details': page_obj, 'query': query})

@group_required('admin')
@login_required
def stocking_detail_create(request):
    if request.method == 'POST':
        form = StockingDetailForm(request.POST)
        if form.is_valid():
            new_detail = form.save()
            return redirect('stocking_detail_list')
    else:
        form = StockingDetailForm()
    return render(request, 'stocking_detail_form.html', {'form': form})

@group_required('admin')
@login_required
def stocking_detail_update(request, pk):
    detail = get_object_or_404(StockingDetail, pk=pk)
    initial_quantity = detail.stocking_quantity
    if request.method == 'POST':
        form = StockingDetailForm(request.POST, instance=detail)
        if form.is_valid():
            updated_detail = form.save()
            return redirect('stocking_detail_list')
    else:
        form = StockingDetailForm(instance=detail)
    return render(request, 'stocking_detail_form.html', {'form': form})

@group_required('admin')
@login_required
def stocking_detail_delete(request, pk):
    detail = get_object_or_404(StockingDetail, pk=pk)
    detail.delete()
    return redirect('stocking_detail_list')

@group_required('admin')
@login_required
def main_course_bom_settings(request):
    if request.method == 'POST':
        form = CourseSidesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main_course_bom_settings')
    else:
        form = CourseSidesForm()
        courses = MainCourse.objects.all()
        course_sides = CourseSides.objects.select_related('course', 'sides').all()
    return render(request, 'main_course_bom_form.html', {
        'form': form,
        'courses': courses,
        'course_sides': course_sides
    })

@group_required('admin')
@login_required
def edit_course_sides(request, pk):
    cs = get_object_or_404(CourseSides, pk=pk)
    if request.method == 'POST':
        form = CourseSidesForm(request.POST, instance=cs)
        if form.is_valid():
            form.save()
            return redirect('main_course_bom_settings')
    else:
        form = CourseSidesForm(instance=cs)
    return render(request, 'course_sides_form.html', {
        'form': form
    })

@group_required('admin')
@login_required
def delete_course_sides(request, pk):
    cs = get_object_or_404(CourseSides, pk=pk)
    cs.delete()
    return redirect('main_course_bom_settings')

@group_required('admin')
@login_required
def edit_course_sides(request, pk):
    cs = get_object_or_404(CourseSides, pk=pk)
    if request.method == 'POST':
        form = CourseSidesForm(request.POST, instance=cs)
        if form.is_valid():
            form.save()
            return redirect('main_course_bom_settings')
    else:
        form = CourseSidesForm(instance=cs)
    return render(request, 'course_sides_form.html', {'form': form})

@group_required('admin')
@login_required
def delete_course_sides(request, pk):
    cs = get_object_or_404(CourseSides, pk=pk)
    cs.delete()
    return redirect('main_course_bom_settings')

@group_required('admin')
@login_required
def inventory_management(request):
    total_patients = Patient.objects.count()
    
    days = int(request.GET.get('days', 7))  

    sides = Sides.objects.all()
    
    inventory_data = []
    for side in sides:
        total_needed = 0
        related_course_sides = CourseSides.objects.filter(sides=side)
        for cs in related_course_sides:
            total_needed += cs.quantity * total_patients * days
        
        inventory_data.append({
            'sides_name': side.sides_name,
           'current_stock': side.current_stock,
            'minimum_required': total_needed,
        })

    return render(request, 'inventory_management.html', {'inventory_data': inventory_data, 'days': days})