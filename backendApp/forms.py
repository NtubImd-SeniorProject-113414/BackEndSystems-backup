from django import forms
from django.core.exceptions import ValidationError
from .models import Medicine,Purchase, Warehouse

class NewMedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['medicine_name', 'efficacy', 'side_effects', 'min_stock_level']
        labels = {
            'medicine_name': '藥品名稱',
            'efficacy': '功效',
            'side_effects': '副作用',
            'min_stock_level': '最低庫存量',
        }
        error_messages = {
            'medicine_name': {'required': '藥品名稱不可為空'},
            'efficacy': {'required': '功效不可為空'},
            'side_effects': {'required': '副作用不可為空'},
            'min_stock_level': {'required': '最低庫存量不可為空'},
        }

    def clean_min_stock_level(self):
        min_stock_level = self.cleaned_data.get('min_stock_level')
        if min_stock_level is not None and min_stock_level <= 0:
            raise ValidationError('最低库存量不可为0')
        return min_stock_level



class NewPurchase(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['medicine', 'purchase_date', 'purchase_q', 'purchase_unit_price']
        labels = {
            'medicine': '藥品名稱',
            'purchase_date': '進貨日期',
            'purchase_q': '進貨數量',
            'purchase_unit_price': '進貨單價',
        }
        error_messages = {
            'medicine': {'required': '藥品名稱不可為空'},
            'purchase_date': {'required': '進貨日期不可為空'},
            'purchase_q': {'required': '進貨數量不可為空'},
            'purchase_unit_price': {'required': '進貨單價不可為空'},
        }

    def clean_purchase_q(self):
        purchase_q = self.cleaned_data.get('purchase_q')
        if purchase_q is not None and purchase_q <= 0:
            raise ValidationError('最低進貨數量不可為0')
        return purchase_q
      
    def clean_purchase_unit_price(self):
        purchase_unit_price = self.cleaned_data.get('purchase_unit_price')
        if purchase_unit_price is not None and purchase_unit_price <= 0:
            raise ValidationError('最低進貨單價不可為0')
        return purchase_unit_price


class WarehouseCreationForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = ['medicine', 'creation_date', 'is_active']
        labels = {
            'medicine': '藥品名稱',
            'creation_date': '創建日期',
            'is_active': '是否啟用',
           }
        widgets = {
            'creation_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'medicine': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }

class WarehouseFilterForm(forms.Form):
    medicine_name = forms.ModelChoiceField(
        queryset=Medicine.objects.all(),
        label='藥品名稱',
        required=False,
        empty_label='--- 不篩選 ---'  # 添加空選項
    )
    is_active = forms.BooleanField(label='是否啟用', required=False)