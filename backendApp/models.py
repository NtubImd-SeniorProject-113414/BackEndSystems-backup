import datetime
import secrets
import uuid
from MySQLdb import IntegrityError
from django.db import models
from django.db.models import Sum


class Medicine(models.Model):
    medicine_id = models.AutoField(primary_key=True)
    medicine_name = models.CharField(max_length=100)
    efficacy = models.TextField()
    side_effects = models.TextField()
    min_stock_level = models.IntegerField()

    def __str__(self):
        return self.medicine_name

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
    def add_new_medicine(cls, name, efficacy, side_effects, min_stock_level):
        try:
            new_medicine = cls(name=name, efficacy=efficacy, side_effects=side_effects, min_stock_level=min_stock_level)
            new_medicine.save()
        except IntegrityError:
            raise IntegrityError("Failed to add medicine.")

    @property
    def stock_status(self):
        if self.min_stock_level > 0:
            return "庫存充足"
        else:
            return "庫存不足"
        
    def get_current_stock(self):
        total_purchased = self.purchase_set.aggregate(total=Sum('purchase_q')).get('total') or 0
        total_dispensed = self.prescriptiondetails_set.aggregate(total=Sum('dispensing_q')).get('total') or 0
        return total_purchased - total_dispensed


class LineBOT(models.Model):
    line_uid = models.CharField(primary_key=True, max_length=100, unique=True)
    name = models.CharField(max_length=100)
    id_card = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    birth = models.DateField()

#處方
class Prescription(models.Model):
    prescription_id = models.AutoField(primary_key=True)
    line_bot = models.ForeignKey(LineBOT, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    barcode = models.CharField(max_length=100, default=uuid.uuid4, unique=True, editable=False)


#進貨
class Purchase(models.Model):
    order_id = models.AutoField(primary_key=True)
    medicine = models.ForeignKey('Medicine', on_delete=models.CASCADE)
    purchase_date = models.DateField()
    purchase_q = models.IntegerField()
    purchase_unit_price = models.IntegerField()


#庫存與車
class Warehouse(models.Model):
    warehouse_id = models.AutoField(primary_key=True)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    creation_date = models.DateField()
    is_active = models.BooleanField(default=True)

#處方明細
class PrescriptionDetails(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name='details')
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    dosage = models.CharField(max_length=100)
    dispensing_q = models.IntegerField()