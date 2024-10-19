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
from django.db.models import Avg,Q
from django.utils.dateparse import parse_date
from django.core.files.base import ContentFile


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
    
    patients_with_forms = [
        {
            'patient': patient,
            'form': PatientFormEdit(instance=patient)
        }
        for patient in page_obj
    ]
    
    return render(request, 'patientManagement/patient_manager.html', {
        'page_obj': page_obj,
        'add_form': PatientForm(),
        'patients_with_forms': patients_with_forms
    })

# 上傳被照護者圖片視圖
@login_required
@group_required('caregiver')
def upload_patient_image(request, patient_id):
    patient = get_object_or_404(Patient, patient_id=patient_id)

    if request.method == 'POST' and request.FILES.get('croppedImage'):
        # 如果已存在舊圖片，先刪除
        if patient.patient_image_path:
            patient.patient_image_path.delete(save=False)  # 刪除舊圖片，但不立即保存

        # 獲取新上傳的文件
        myfile = request.FILES['croppedImage']
        
        # 生成 UUID 檔案名，並保留文件的副檔名
        ext = myfile.name.split('.')[-1]  # 取得文件的副檔名
        new_filename = f"{uuid.uuid4()}.{ext}"  # 生成唯一的 UUID 檔案名

        # 使用 ImageField 保存新圖片，並使用 UUID 作為檔名
        patient.patient_image_path.save(new_filename, ContentFile(myfile.read()), save=True)

        # 獲取圖片的 URL
        file_url = patient.patient_image_path.url
        
        return JsonResponse({'url': file_url})
    
    return JsonResponse({'error': '圖片上傳失敗'}, status=400)

# 刪除被照護者照片
@login_required
@group_required('caregiver')
def delete_patient_image(request, patient_id):
    if request.method == 'POST':
        patient = get_object_or_404(Patient, patient_id=patient_id)

        # 確認患者是否有圖片
        if patient.patient_image_path:
            # 刪除圖片文件
            patient.patient_image_path.delete(save=True)
            return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'fail'}, status=400)

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


#情緒管理所有情緒紀錄
@group_required('caregiver')
@login_required
def chatlogs_view(request):
    # 獲取篩選條件
    patient_name = request.GET.get('patient_name', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')
    search_query = request.GET.get('search', '')

    # 基本查詢集
    chatlogs_list = ChatLogs.objects.all().order_by('-created_time')

    # 篩選條件
    if patient_name:
        chatlogs_list = chatlogs_list.filter(patient__patient_name__icontains=patient_name)

    if start_date:
        chatlogs_list = chatlogs_list.filter(created_time__date__gte=parse_date(start_date))
    
    if end_date:
        chatlogs_list = chatlogs_list.filter(created_time__date__lte=parse_date(end_date))

    if search_query:
        chatlogs_list = chatlogs_list.filter(patient_message__icontains=search_query)

    # 每頁顯示10筆記錄
    paginator = Paginator(chatlogs_list, 10)

    # 獲取當前頁碼，默認為第1頁
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # 將篩選條件傳遞回模板，方便保持篩選條件狀態
    context = {
        'page_obj': page_obj,
        'patient_name': patient_name,
        'start_date': start_date,
        'end_date': end_date,
        'search_query': search_query
    }

    return render(request, 'emotion/chatlogs.html', context)

# 情緒平均狀況
@group_required('caregiver')
@login_required
def patient_emotion_view(request):
    # 取得篩選條件
    selected_patient = request.GET.get('patient', '')  # 篩選條件：被照護者

    # 計算每個患者的平均情緒分數，並根據名稱篩選
    patients = Patient.objects.annotate(avg_emotion_score=Avg('chatlogs__emotion_score')).order_by('-avg_emotion_score')

    if selected_patient:
        patients = patients.filter(Q(patient_name__icontains=selected_patient))

    # 每頁顯示10筆記錄
    paginator = Paginator(patients, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # 預設星星數量和邏輯處理
    for patient in page_obj:
        if patient.avg_emotion_score is None:
            patient.avg_emotion_score = 0  # 預設為0，沒有數據則顯示灰色
        patient.full_stars = list(range(int(patient.avg_emotion_score)))  # 完整愛心範圍
        patient.half_star = (patient.avg_emotion_score - int(patient.avg_emotion_score)) >= 0.5  # 半顆愛心
        patient.empty_stars = list(range(5 - len(patient.full_stars) - (1 if patient.half_star else 0)))  # 空愛心範圍

    return render(request, 'emotion/patient_emotions.html', {
        'page_obj': page_obj,
        'selected_patient': selected_patient,
    })


# 負面情緒顯示
@group_required('caregiver')
@login_required
def negative_chatlogs_view(request):
    negative_logs = ChatLogs.objects.filter(emotion_score__lte=1, is_confirmed=False).order_by('-created_time')

    # 每頁顯示 15 條記錄
    paginator = Paginator(negative_logs, 15)  
    page_number = request.GET.get('page', 1)  # 獲取當前頁碼，默認為第 1 頁
    page_obj = paginator.get_page(page_number)  # 分頁對象

    return render(request, 'emotion/negative_chatlogs.html', {'page_obj': page_obj})

#已處理負面紀錄
@group_required('caregiver')
@login_required
def confirm_chatlog(request, chatlog_id):
    if request.method == 'POST':
        try:
            chatlog = ChatLogs.objects.get(pk=chatlog_id)
            chatlog.is_confirmed = True
            chatlog.confirmed_time = timezone.now()  # 設置處理時間
            chatlog.save()
            return JsonResponse({'status': 'success'})
        except ChatLogs.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': '記錄不存在'})
    return JsonResponse({'status': 'error', 'message': '無效請求'})

# 已處理的負面情緒記錄視圖
@group_required('caregiver')
@login_required
def confirmed_negative_logs_view(request):
    logs_list = ChatLogs.objects.filter(emotion_score__lte=2, is_confirmed=True).order_by('-confirmed_time')
    
    # 使用 Paginator 進行分頁，每頁顯示15筆記錄
    paginator = Paginator(logs_list, 15)
    
    # 獲取當前頁碼，默認為第1頁
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, 'emotion/confirmed_negative_chatlogs.html', {'page_obj': page_obj})

@group_required('caregiver')
@login_required
def dashboard_data(request):
    # Only show vehicles that are not 'offline'
    vehicles = Vehicle.objects.filter(~Q(vehicle_status__vehicle_status_name='offline'))[:3]

    # Only show orders that have not been completed
    orders = Order.objects.filter(order_state__order_state_name='pending').order_by('-order_time')[:3]

    # Existing logic for notifications and patients
    notifications = ChatLogs.objects.filter(emotion_score=1, is_confirmed=False).order_by('-created_time')[:5]
    patients = Patient.objects.annotate(avg_emotion_score=Avg('chatlogs__emotion_score')).order_by('-avg_emotion_score')[:3]
    patient_count = Patient.objects.count()

    data = {
        'vehicles': [
            {
                'name': v.vehicle_name,
                'status': v.vehicle_status.vehicle_state_html_style
            } for v in vehicles
        ],
        'orders': [
            {
                'id': o.order_id,
                'patient': o.patient.patient_name,
                'course': o.course.course_name,
                'quantity': o.order_quantity,
                'time': o.order_time.strftime('%Y-%m-%d %H:%M:%S'),
                'state': o.order_state.order_state_name
            } for o in orders
        ],
        'notifications': [
            {
                'patient': n.patient.patient_name,
                'emotion_score': n.emotion_score,
                'is_confirmed': n.is_confirmed
            } for n in notifications
        ],
        'patients': [
            {
                'name': p.patient_name,
                'avg_emotion_score': p.avg_emotion_score or 0
            } for p in patients
        ],
        'patient_count': patient_count
    }

    return JsonResponse(data)