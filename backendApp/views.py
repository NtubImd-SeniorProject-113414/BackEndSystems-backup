from django import forms
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Medicine, PrescriptionDetails, User_Account, Warehouse
from django.http import JsonResponse
from django.db import IntegrityError


def index(request):
    username = request.user.Name if request.user.is_authenticated else "Guest"
    context = {'username': username}
    return render(request, 'index.html', context)

def medicine_list(request):
    medicines = Medicine.objects.all()
    return render(request, 'medicine_list.html', {'medicines': medicines})

def delete_medicine(request, medicine_id):
    medicine = get_object_or_404(Medicine, pk=medicine_id)
    medicine.delete()
    return redirect('medicine_list')


class NewMedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['medicine_name', 'efficacy', 'side_effects', 'stock_level']

def add_medicine(request):
    if request.method == 'POST':
        form = NewMedicineForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '藥品添加成功！')
            return redirect('medicine_list')
        else:
            messages.error(request, '請檢查輸入的數據.')
            return render(request, 'add_medicine.html', {'form': form, 'medicines': Medicine.objects.all()})
    else:
        form = NewMedicineForm()
    return render(request, 'add_medicine.html', {'form': form, 'medicines': Medicine.objects.all()})

def warehouse_list(request):
    warehouses = Warehouse.objects.all()
    return render(request, 'warehouse.html', {'warehouses': warehouses})

class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = ['medicine', 'is_active']

def toggle_warehouse_status(request, warehouse_id):
    warehouse = get_object_or_404(Warehouse, pk=warehouse_id)
    warehouse.is_active = not warehouse.is_active
    warehouse.save()
    return JsonResponse({'status': 'success', 'is_active': warehouse.is_active})

def show_stock(request):
    medicines = Medicine.objects.all()
    return render(request, 'show_stock.html', {'medicines': medicines})