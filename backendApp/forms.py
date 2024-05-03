from django import forms
from django.core.exceptions import ValidationError
from .models import CourseSides, MainCourse, Medicine, Patient,Purchase, Sides, Stocking, StockingDetail, Supplier, Warehouse,Bed, MealOrderTimeSlot
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User,Group


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
            raise ValidationError('最低庫存量不可為0')
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
        empty_label='--- 不篩選 ---'  
    )
    is_active = forms.BooleanField(label='是否啟用', required=False)

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='必填，請輸入有效的郵件地址。')
    first_name = forms.CharField(max_length=30, required=True, help_text='必填')
    last_name = forms.CharField(max_length=30, required=True, help_text='必填')
    is_active = forms.BooleanField(required=False, help_text='選擇是否啟用帳戶')
    is_superuser = forms.BooleanField(required=False, help_text='選擇是否設為超級用戶')
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        help_text='選擇用戶所屬的群組。'
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'is_active', 'is_superuser', 'groups')

    def clean_prdfilo(self):
        email = self.email
        first_name = self.first_name
        last_name = self.last_name
        if not first_name and last_name:
            raise forms.ValidationError("姓名是必填項")
        elif not email:
            raise forms.ValidationError("電子郵件是必填項")
        return email + first_name + last_name

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.is_active = self.cleaned_data['is_active']
        user.is_superuser = self.cleaned_data['is_superuser']
        user.is_staff = self.cleaned_data['is_superuser'] 
        if commit:
            user.save()
            user.groups.set(self.cleaned_data['groups'])
        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['patient_name', 'patient_birth', 'patient_number','patient_idcard']
        widgets = {
            'patient_birth': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }

class BedForm(forms.ModelForm):
    class Meta:
        model = Bed
        fields = ['bed_number', 'patient']


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['supplier_name', 'supplier_number']


class MainCourseForm(forms.ModelForm):
    timeSlot = forms.ModelChoiceField(queryset=MealOrderTimeSlot.objects.all(), empty_label=None)
    class Meta:
        model = MainCourse
        fields = ['course_name', 'course_price', 'course_stock', 'course_image', 'timeSlot']

class CourseSidesForm(forms.ModelForm):
    class Meta:
        model = CourseSides
        fields = ['course', 'sides', 'quantity']

class StockingForm(forms.ModelForm):
    class Meta:
        model = Stocking
        fields = ['supplier']

class StockingDetailForm(forms.ModelForm):
    new_sides_name = forms.CharField(max_length=100, required=False, help_text='輸入新的配菜名稱')
    supplier = forms.ModelChoiceField(queryset=Supplier.objects.all(), required=True, help_text='選擇供應商')
    # 日期選擇器用於進貨日期
    stocking_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), help_text='選擇進貨日期')

    class Meta:
        model = StockingDetail
        fields = ['stocking_quantity', 'stocking_date']

    def save(self, commit=True):
        # 根據新的配菜名稱創建或找到現有的 Sides 實例
        new_sides_name = self.cleaned_data.get('new_sides_name')
        if new_sides_name:
            sides, created = Sides.objects.get_or_create(sides_name=new_sides_name)
            self.instance.sides = sides  # 正確的是 'sides' 不是 'side'
        
        # 根據選擇的供應商創建或找到現有的 Stocking 實例
        supplier = self.cleaned_data.get('supplier')
        stocking, created = Stocking.objects.get_or_create(supplier=supplier)
        self.instance.stocking = stocking
        
        return super().save(commit=commit)