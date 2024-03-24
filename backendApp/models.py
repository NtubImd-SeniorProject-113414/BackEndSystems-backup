import datetime
from MySQLdb import IntegrityError
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class User_Account(AbstractBaseUser):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True)
    account = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)

    USERNAME_FIELD = 'account'  # 指定用户名字段为 account

class Medicine(models.Model):
    medicine_id = models.AutoField(primary_key=True)
    medicine_name = models.CharField(max_length=100)
    efficacy = models.TextField()
    side_effects = models.TextField()
    stock_level = models.IntegerField()

    @staticmethod
    def deleteMedicine(medicine_id):
        try:
            medicine_to_delete = Medicine.objects.get(medicine_id=medicine_id)
            medicine_to_delete.delete()
            return "刪除成功"
        except Medicine.DoesNotExist:
            return "藥品不存在"
        except Exception as e:
            return f"刪除失敗: {e}"

    @classmethod
    def add_new_medicine(cls, name, efficacy, side_effects, stock_level):
        try:
            new_medicine = cls(name=name, efficacy=efficacy, side_effects=side_effects, stock_level=stock_level)
            new_medicine.save()
        except IntegrityError:
            raise IntegrityError("Failed to add medicine.")


    @property
    def stock_status(self):
        if self.stock_level > 0:
            return "庫存充足"
        else:
            return "庫存不足"


class LineBOT(models.Model):
    line_uid = models.CharField(primary_key=True, max_length=100, unique=True)
    name = models.CharField(max_length=100)
    id_card = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    birth = models.DateField()


class Prescription(models.Model):
    prescription_id = models.AutoField(primary_key=True)
    line_bot = models.ForeignKey(LineBOT, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    medicines = models.ManyToManyField(Medicine)  # 新增 ManyToManyField 關係

class Purchase(models.Model):
    order_id = models.AutoField(primary_key=True)
    medicine = models.ForeignKey('Medicine', on_delete=models.CASCADE)
    purchase_date = models.DateField(auto_now_add=True)
    purchase_q = models.IntegerField()
    purchase_unit_price = models.IntegerField()



class StockChange(models.Model):
    CHANGE_TYPES = (
        ('increase', 'Increase'),
        ('decrease', 'Decrease'),
    )
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    change_type = models.CharField(max_length=20, choices=CHANGE_TYPES)
    quantity = models.IntegerField()
    change_date = models.DateField(auto_now_add=True)
    description = models.CharField(max_length=255)

    @classmethod
    def create(cls, medicine, change_type, quantity, description=''):
        stock_change = cls(medicine=medicine, change_type=change_type, quantity=quantity, description=description)
        if change_type == 'increase':
            medicine.stock_level += quantity
        elif change_type == 'decrease':
            medicine.stock_level -= quantity
        medicine.save()
        stock_change.save()
        return stock_change


class Warehouse(models.Model):
    warehouse_id = models.AutoField(primary_key=True)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    creation_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

class PrescriptionDetails(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name='details')
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    dosage = models.CharField(max_length=100)
    dispensing_q = models.IntegerField()