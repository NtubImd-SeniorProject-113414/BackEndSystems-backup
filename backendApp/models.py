import os
import uuid
from django.utils import timezone
from django.db import models
from django.db.models import Sum
from datetime import datetime, time


class Medicine(models.Model):
    medicine_id = models.AutoField(primary_key=True)
    medicine_name = models.CharField(max_length=100)
    efficacy = models.TextField()
    side_effects = models.TextField()
    min_stock_level = models.IntegerField()

    def __str__(self):
        return self.medicine_name

    def get_current_stock(self):
        total_purchased = self.purchase_set.aggregate(total=Sum('purchase_q')).get('total') or 0
        total_dispensed = self.prescriptiondetails_set.aggregate(total=Sum('dispensing_q')).get('total') or 0
        return total_purchased - total_dispensed

#處方
class Prescription(models.Model):
    prescription_id = models.AutoField(primary_key=True)
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
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)
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
    patient_idcard =models.CharField(max_length=10)
    line_notify = models.CharField(max_length=45, blank=True, null=True, unique=True)
    line_id = models.CharField(max_length=45, blank=True, null=True, unique=True)
    created_time = models.DateTimeField(auto_now_add=False, default=timezone.now)

    @staticmethod
    def getpatientIdByLineUid(line_uid):
        matching_patient = Patient.objects.filter(line_id=line_uid).first()
        return matching_patient.patient_id if matching_patient else None
    
    @staticmethod
    def createLineAccount(name, idcard, phone, lineUid):
        if Patient.getpatientIdByLineUid(lineUid):
            return {"status": True, "msg":"此LINE帳戶已經驗證"}
        try:
            patient = Patient.objects.get(patient_name=name, patient_idcard=idcard, patient_number=phone)
            patient.line_id = lineUid
            patient.save()
            return {"status": True, "msg":"驗證成功!"}
            
        except Patient.DoesNotExist:
            return {"status": False, "msg":"資料填寫錯誤"}
    def __str__(self):
        return self.patient_name

#RFID卡片
class RfidCard(models.Model):
    RfidCard_code = models.CharField(primary_key=True, max_length=50)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=False, default=timezone.now)

#點餐時段
class MealOrderTimeSlot(models.Model):
    timeSlot_id = models.AutoField(primary_key=True)
    timeSlot_name = models.CharField(max_length=3)
    startTime = models.TimeField(default='00:00')
    deadlineTime = models.TimeField(default='00:00')
    endTimes = models.TimeField(default='00:00')
    def __str__(self):
        return f'{self.timeSlot_name} ({self.startTime} - {self.endTimes})'
    
    #尋找與現在時間相符的時段
    @staticmethod
    def find_time_slot(formatted_time):
        hour, minute = map(int, formatted_time.split(':'))
        current_time = time(hour, minute)
        time_slots = MealOrderTimeSlot.objects.all()
        for time_slot in time_slots:
            if time_slot.startTime <= current_time <= time_slot.endTimes:
                return time_slot
        return None 
    
    #尋找離現在時間最近的下個時段
    @staticmethod
    def find_nearest_time_slot(nowTimeSlot, formatted_time):
        nowHour, nowMinute = map(int, formatted_time.split(':'))
        current_time = time(nowHour, nowMinute)
        time_slots = MealOrderTimeSlot.objects.all()
        nearest_time_slot = None
        min_distance = float('inf')
        for time_slot in time_slots:
            if current_time <= time_slot.endTimes:
                start_distance = abs((current_time.hour * 60 + current_time.minute) - (time_slot.startTime.hour * 60 + time_slot.startTime.minute))
                end_distance = abs((current_time.hour * 60 + current_time.minute) - (time_slot.endTimes.hour * 60 + time_slot.endTimes.minute))
                if start_distance < min_distance and time_slot != nowTimeSlot:
                    min_distance = start_distance
                    nearest_time_slot = time_slot
                if end_distance < min_distance and time_slot != nowTimeSlot:
                    min_distance = end_distance
                    nearest_time_slot = time_slot
        min_distance = float('inf')
        if nearest_time_slot == None:
            for time_slot in time_slots:
                start_distance = (time_slot.startTime.hour * 60 + time_slot.startTime.minute)
                if start_distance < min_distance:
                    nearest_time_slot = time_slot
                    min_distance = start_distance
        return nearest_time_slot

def course_image_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('img', new_filename)

#主餐
class MainCourse(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=45)
    course_price = models.IntegerField()
    course_image = models.ImageField(upload_to=course_image_upload_to, blank=True, null=True)
    created_time = models.DateTimeField(auto_now_add=False, default=timezone.now)
    timeSlot = models.ForeignKey(MealOrderTimeSlot, on_delete=models.CASCADE)

    def __str__(self):
        return self.course_name

    def calculate_bom(self, number_of_patients, days):
        bom_results = {}
        course_sides = self.course_sides.all()
        for cs in course_sides:
            total_needed = cs.quantity * number_of_patients * days
            bom_results[cs.sides.sides_name] = total_needed
        return bom_results
    
#訂單狀態
class OrderState(models.Model):
    OrderState_code = models.AutoField(primary_key=True)
    OrderState_name = models.CharField(max_length=10)
    OrderState_htmlStyle = models.CharField(max_length=100)

#訂單
class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    course = models.ForeignKey(MainCourse, on_delete=models.CASCADE, db_column='course_id')
    orderState = models.ForeignKey(OrderState, on_delete=models.CASCADE, db_column='OrderState_code', related_name='orders')
    order_quantity = models.IntegerField()
    order_time = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def getOrderByPatientIdAndTimeSlot(patient_id, timeSlot):
        today = datetime.today()
        start_time = datetime.combine(today, timeSlot.startTime)
        end_time = datetime.combine(today, timeSlot.deadlineTime)
        return Order.objects.filter(patient_id=patient_id, order_time__range=(start_time, end_time))

#配菜
class Sides(models.Model):
    sides_id = models.AutoField(primary_key=True)
    sides_name = models.CharField(max_length=45)
    created_time = models.DateTimeField(auto_now_add=False, default=timezone.now)

    def __str__(self):
        return self.sides_name


#主餐與配菜
class CourseSides(models.Model):
    coursesides_id = models.AutoField(primary_key=True)
    course = models.ForeignKey(MainCourse, related_name='course_sides', on_delete=models.CASCADE, db_column='course_id')
    sides = models.ForeignKey(Sides, on_delete=models.CASCADE, db_column='sides_id')
    quantity = models.IntegerField() 
    created_time = models.DateTimeField(auto_now_add=False, default=timezone.now)

    @staticmethod
    def calculateTotalQuantityBySideId(sides_id):
        sides = Sides.objects.get(sides_id=sides_id)
        course_sides = CourseSides.objects.filter(sides=sides)
        total_quantity = 0
        for course_side in course_sides:
            print(course_side.course.course_name)
            order_quantity = Order.objects.filter(course=course_side.course)
            print(order_quantity)
            # if order_quantity:
            #     total_quantity += order_quantity * course_side.quantity
        return total_quantity


#床位
class Bed(models.Model):
    bed_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, blank=True, null=True)
    bed_number = models.CharField(max_length=5, unique=True, null=True, blank=True)
    created_time = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.bed_number

#進貨
class Stocking(models.Model):
    stocking_id = models.AutoField(primary_key=True)
    supplier = models.ForeignKey('Supplier', on_delete=models.CASCADE, db_column='supplier_id')
    created_time = models.DateTimeField(auto_now_add=False, default=timezone.now)


#進貨明細
class StockingDetail(models.Model):
    stocking_detail_id = models.AutoField(primary_key=True)
    stocking = models.ForeignKey(Stocking, on_delete=models.CASCADE, db_column='stocking_id')
    sides = models.ForeignKey(Sides, on_delete=models.CASCADE, db_column='sides_id')
    stocking_quantity = models.IntegerField()
    stocking_date = models.DateTimeField(auto_now_add=False)
    created_time = models.DateTimeField(auto_now_add=False, default=timezone.now)

    @staticmethod
    def getSidesQuantityBySides(sides):
        total_quantity = StockingDetail.objects.filter(sides=sides).aggregate(Sum('stocking_quantity'))['stocking_quantity__sum']
        return total_quantity if total_quantity is not None else 0

    def __str__(self):
        return f"{self.sides.sides_name} - {self.stocking_quantity}"

#供應商
class Supplier(models.Model):
    supplier_id = models.AutoField(primary_key=True)
    supplier_name = models.CharField(max_length=45)
    supplier_number = models.CharField(max_length=10, blank=True, null=True)
    line_notify = models.CharField(max_length=45, blank=True, null=True)
    created_time = models.DateTimeField(auto_now_add=False, default=timezone.now)

    def __str__(self):
        return self.supplier_name

#通知
class Notify(models.Model):
    notify_id = models.AutoField(primary_key=True)
    notify_message = models.CharField(max_length=1000)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=False, default=timezone.now)

#虛擬人聊天紀錄
class ChatLogs(models.Model):
    chatLog_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    patient_message = models.CharField(max_length=1000)
    response_message = models.CharField(max_length=1000)
    created_time = models.DateTimeField(auto_now_add=False, default=timezone.now)

#用藥需求狀態
class MedicineDemandState(models.Model):
    MedicineDemandState_code = models.AutoField(primary_key=True)
    OrderState_name = models.CharField(max_length=10)

#用藥需求
class MedicineDemand(models.Model):
    medicineDemand_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    patient_demand = models.CharField(max_length=300)
    MedicineDemandState = models.ForeignKey(MedicineDemandState, on_delete=models.CASCADE, db_column='MedicineDemandState_code')
    review_time = models.DateTimeField(auto_now_add=False, default=timezone.now)
    created_time = models.DateTimeField(auto_now_add=False, default=timezone.now)

#車子
class Vehicle(models.Model):
    Vehicle_id = models.AutoField(primary_key=True)
    Vehicle_status = models.ForeignKey(MedicineDemandState, on_delete=models.CASCADE, db_column='VehicleStatus_code')
    created_time = models.DateTimeField(auto_now_add=False, default=timezone.now)

#車子狀態
class VehicleStatus(models.Model):
    VehicleStatus_code = models.AutoField(primary_key=True)
    VehicleStatus_name = models.CharField(max_length=10)
