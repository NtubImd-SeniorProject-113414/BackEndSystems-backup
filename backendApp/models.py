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


#---------------------------
#被照顧者
class Patient(models.Model):
    patient_id = models.AutoField(primary_key=True)
    patient_name = models.CharField(max_length=45)
    patient_birth  = models.DateField()
    patient_number = models.CharField(max_length=10)
    line_notify = models.CharField(max_length=45, blank=True, null=True)
    line_id = models.CharField(max_length=45, blank=True, null=True)
    created_time = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def checkLineRegister(lineUid):
        matching_patients = Patient.objects.filter(line_id=lineUid)
        return matching_patients.exists()
    
    @staticmethod
    def createLineAccount(name, patient_number, phone, lineUid):
        if Patient.checkLineRegister(lineUid):
            return {"status": True, "msg":"此LINE帳戶已經驗證"}
        try:
            patient = Patient.objects.get(patient_name=name, patient_number=patient_number)
            patient.line_id = lineUid
            patient.save()
            return {"status": True, "msg":"驗證成功!"}
            
        except Patient.DoesNotExist:
            return {"status": False, "msg":"資料填寫錯誤"}
    def __str__(self):
        return self.patient_name

#主餐
class MainCourse(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=45)
    course_price = models.IntegerField()
    course_stock = models.IntegerField()
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.course_name

#訂單
class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    course = models.ForeignKey(MainCourse, on_delete=models.CASCADE, db_column='course_id')
    order_quantity = models.IntegerField()
    order_date = models.DateTimeField(auto_now_add=True)
    

#主餐與配菜
class CourseSides(models.Model):
    sides_id = models.AutoField(primary_key=True)
    course = models.ForeignKey(MainCourse, related_name='course_sides', on_delete=models.CASCADE, db_column='course_id')
    created_time = models.DateTimeField(auto_now_add=True)


#床位
class Bed(models.Model):
    bed_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, db_column='patient_id')
    bed_number = models.CharField(max_length=5)  # Optional: Add a bed number or other attributes
    created_time = models.DateTimeField(auto_now_add=True)

#配菜
class Sides(models.Model):
    sides_id = models.AutoField(primary_key=True)
    sides_name = models.CharField(max_length=45)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sides_name

#進貨
class Stocking(models.Model):
    stocking_id = models.AutoField(primary_key=True)
    supplier = models.ForeignKey('Supplier', on_delete=models.CASCADE, db_column='supplier_id')
    created_time = models.DateTimeField(auto_now_add=True)


#進貨明細
class StockingDetail(models.Model):
    stocking_detail_id = models.AutoField(primary_key=True)
    stocking = models.ForeignKey(Stocking, on_delete=models.CASCADE, db_column='stocking_id')
    sides = models.ForeignKey(Sides, on_delete=models.CASCADE, db_column='sides_id')
    stocking_quantity = models.IntegerField()
    stocking_date = models.DateTimeField(auto_now_add=True)
    created_time = models.DateTimeField(auto_now_add=True)

#供應商
class Supplier(models.Model):
    supplier_id = models.AutoField(primary_key=True)
    supplier_name = models.CharField(max_length=45)
    supplier_number = models.CharField(max_length=10, blank=True, null=True)
    line_notify = models.CharField(max_length=45, blank=True, null=True)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.supplier_name

#送餐
class Delivery(models.Model):
    delivery_id = models.AutoField(primary_key=True)
    bed = models.ForeignKey(Bed, on_delete=models.CASCADE, db_column='bed_id')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, db_column='order_id')
    status = models.SmallIntegerField(default=0)
    created_time = models.DateTimeField(auto_now_add=True)
