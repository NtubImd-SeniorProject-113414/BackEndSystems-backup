from django.db import models

#被照顧者
class Patient(models.Model):
    patient_id = models.AutoField(primary_key=True)
    patient_name = models.CharField(max_length=45)
    allergy = models.CharField(max_length=100, blank=True, null=True)
    line_notify = models.CharField(max_length=45, blank=True, null=True)
    line_id = models.CharField(max_length=45, blank=True, null=True)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.patient_name

#主餐
class MainCourse(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=45)
    course_price = models.IntegerField()
    course_stock = models.IntegerField()

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

#床位
class Bed(models.Model):
    bed_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, db_column='patient_id')

#配菜
class Sides(models.Model):
    sides_id = models.AutoField(primary_key=True)
    sides_name = models.CharField(max_length=45)

    def __str__(self):
        return self.sides_name

#進貨
class Stocking(models.Model):
    stocking_id = models.AutoField(primary_key=True)
    supplier = models.ForeignKey('Supplier', on_delete=models.CASCADE, db_column='supplier_id')

#進貨明細
class StockingDetail(models.Model):
    stocking_detail_id = models.AutoField(primary_key=True)
    stocking = models.ForeignKey(Stocking, on_delete=models.CASCADE, db_column='stocking_id')
    sides = models.ForeignKey(Sides, on_delete=models.CASCADE, db_column='sides_id')
    stocking_quantity = models.IntegerField()
    stocking_date = models.DateTimeField(auto_now_add=True)

#供應商
class Supplier(models.Model):
    supplier_id = models.AutoField(primary_key=True)
    supplier_name = models.CharField(max_length=45)
    supplier_number = models.CharField(max_length=10, blank=True, null=True)
    line_notify = models.CharField(max_length=45, blank=True, null=True)

    def __str__(self):
        return self.supplier_name

#送餐
class Delivery(models.Model):
    delivery_id = models.AutoField(primary_key=True)
    bed = models.ForeignKey(Bed, on_delete=models.CASCADE, db_column='bed_id')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, db_column='order_id')
    status = models.SmallIntegerField(default=0)