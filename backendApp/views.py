import datetime
import json
from django.contrib import messages
from django.http import HttpResponseForbidden, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from jsonschema import ValidationError
from django.db.models import F
from backendApp.decorator import group_required
from backendApp.middleware import login_required
from .models import Medicine, PrescriptionDetails,  Purchase, PrescriptionDetails,Warehouse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import NewMedicineForm, WarehouseCreationForm,WarehouseFilterForm,UserProfileForm
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User,Group



@group_required('caregiver', 'admin','pharmacy_admin')
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

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('index') 
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'edit_profile.html', {'form': form})


  
#藥品管理
@csrf_exempt
@group_required('pharmacy_admin')
@login_required
def medicine_list(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        medicine_id = data.get('medicine_id')
        medicine_name = data.get('medicine_name')
        efficacy = data.get('efficacy')
        side_effects = data.get('side_effects')
        min_stock_level = data.get('min_stock_level')

        try:
            medicine = Medicine.objects.get(pk=medicine_id)
            medicine.medicine_name = medicine_name
            medicine.efficacy = efficacy
            medicine.side_effects = side_effects
            
            min_stock_level = int(min_stock_level)
            if min_stock_level <= 0:
                return JsonResponse({'status': 'error', 'message': '最小庫存不能小於0'})
            medicine.min_stock_level = min_stock_level
            medicine.full_clean() 
            medicine.save()
            return JsonResponse({'status': 'success'})
        except (ValueError, ValidationError):
            return JsonResponse({'status': 'error', 'message': '最小庫存必須是一個數字'})
        except Medicine.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': '找不到藥品'})

    
    else:
        search_query = request.GET.get('search', '') 
        order_by = request.GET.get('order_by', 'medicine_name') 

        if order_by not in ['medicine_name', 'min_stock_level', 'efficacy', 'side_effects']:
            order_by = 'medicine_name'


        medicines_query = Medicine.objects.filter(
            Q(medicine_name__icontains=search_query) | 
            Q(efficacy__icontains=search_query) | 
            Q(side_effects__icontains=search_query)
        ).order_by(order_by)

        paginator = Paginator(medicines_query, 10) 
        page = request.GET.get('page')
        try:
            medicines = paginator.page(page)
        except PageNotAnInteger:
            medicines = paginator.page(1)
        except EmptyPage:
            medicines = paginator.page(paginator.num_pages)

        return render(request, 'medicine_list.html', {'medicines': medicines})

#刪除藥品
@group_required('pharmacy_admin')
@login_required
def delete_medicine(request, medicine_id):
    if request.method == 'POST':
        medicine_instance = get_object_or_404(Medicine, medicine_id=medicine_id)
        medicine_instance.delete()
        messages.success(request, '藥品刪除成功！')
        return redirect('medicine_list')
    else:
        return HttpResponseForbidden("Forbidden")

#修改藥品
@group_required('pharmacy_admin')
@login_required
def modify_medicine(request, medicine_id):
    medicine = get_object_or_404(Medicine, id=medicine_id)
    if request.method == 'POST':
        form = NewMedicineForm(request.POST, instance=medicine)
        if form.is_valid():
            form.save()
            messages.success(request, '藥品修改成功！')
            return render(request, 'medicine_list.html', {'medicines': Medicine.objects.all()})
    else:
        form = NewMedicineForm(instance=medicine)
    return render(request, 'modify_medicine.html', {'form': form})

#新增藥品
@group_required('pharmacy_admin')
@login_required
def add_medicine(request):
    if request.method == 'POST':
        form = NewMedicineForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '藥品添加成功！')
            return redirect('add_medicine')
        else:
            messages.error(request, '請檢查您所輸入的內容是否正確')
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{form.fields[field].label}: {error}")
    else:
        form = NewMedicineForm()

    return render(request, 'add_medicine.html', {'form': form})

#新增進貨
@group_required('pharmacy_admin')
@login_required
def add_purchase(request):
    medicines = Medicine.objects.all() 

    sort_by = request.GET.get('sort', 'purchase_date')
    if sort_by == 'date_desc':
        order = '-purchase_date' 
    else:
        order = 'purchase_date' 

    purchases = Purchase.objects.all().order_by(order)  

    paginator = Paginator(purchases, 10) 
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    if request.method == 'POST':
        # Extract data from POST request
        medicine_id = request.POST.get('medicine')
        purchase_date = request.POST.get('purchase_date')
        purchase_q = request.POST.get('purchase_q')
        purchase_unit_price = request.POST.get('purchase_unit_price')

        try:
            # Attempt to create and save a new Purchase instance
            Purchase.objects.create(
                medicine_id=medicine_id,
                purchase_date=purchase_date,
                purchase_q=purchase_q,
                purchase_unit_price=purchase_unit_price
            )
            messages.success(request, '進貨添加成功！')
        except Exception as e:
            messages.error(request, f'進貨添加失敗：{str(e)}')

        return redirect('add_purchase')  # Redirect to the same page to show the updated table

    return render(request, 'add_purchase.html', {'medicines': medicines, 'page_obj': page_obj})

@group_required('pharmacy_admin')
@require_POST
@login_required
def delete_purchase(request, order_id):
    Purchase.objects.get(pk=order_id).delete()
    return redirect(request.META.get('HTTP_REFERER', 'add_purchase'))



#庫存與車狀態查看
@group_required('pharmacy_admin')
@login_required
def warehouse_view(request):
    filter_form = WarehouseFilterForm(request.GET or None)
    creation_form = WarehouseCreationForm(request.POST or None)
    warehouses = Warehouse.objects.all()

    # 處理篩選表單
    if request.method == 'GET' and filter_form.is_valid():
        if filter_form.cleaned_data.get('is_active') is not None:
            warehouses = warehouses.filter(is_active=filter_form.cleaned_data['is_active'])

    # 處理新增倉庫表單
    if request.method == 'POST' and creation_form.is_valid():
        creation_form.save()
        return redirect('warehouse')  # 假設 'warehouse_view' 是這個視圖的名字

    # 計算當前庫存和最低庫存水平
    for warehouse in warehouses:
        warehouse.current_stock = warehouse.medicine.get_current_stock()
        warehouse.min_stock_level = warehouse.medicine.min_stock_level

    low_stock_medicines = [warehouse.medicine for warehouse in warehouses if warehouse.current_stock <= warehouse.min_stock_level]

    # 確定警示顏色和消息文本
    alert_color = 'success' if not low_stock_medicines else 'danger'
    alert_message = '目前並無庫存不足狀況。' if not low_stock_medicines else ''

    return render(request, 'warehouse.html', {
        'filter_form': filter_form,
        'creation_form': creation_form,
        'warehouses': warehouses,
        'low_stock_medicines': low_stock_medicines,
        'alert_color': alert_color,
        'alert_message': alert_message
    })

@group_required('pharmacy_admin')
@require_POST
@login_required
def toggle_active(request, warehouse_id):
    warehouse = Warehouse.objects.get(pk=warehouse_id)
    warehouse.is_active = not warehouse.is_active
    warehouse.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@group_required('pharmacy_admin')
@require_POST
@login_required
def delete_warehouse(request, warehouse_id):
    Warehouse.objects.get(pk=warehouse_id).delete()
    return redirect(request.META.get('HTTP_REFERER', 'warehouse'))