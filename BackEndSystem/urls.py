"""
URL configuration for BackEndSystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from django.contrib import admin
from backendApp.views import index, edit_profile
from backendApp.login import login_view,logout_view
from backendApp.account import register
from backendApp.caresystem_views import add_bed, add_main_course, add_patient, add_supplier, bed_manager, caregiver_manager, delete_bed, delete_course_sides, delete_main_course, delete_patient, delete_supplier, edit_bed,edit_caregiver, edit_course_sides, edit_main_course, edit_patient, edit_supplier, inventory_management, main_course_bom_settings, main_course_list, patient_manager, purchase_detail_create, purchase_detail_delete, purchase_detail_list, purchase_detail_update, supplier_list
from backendApp.caresystem_views import add_bed, add_patient, bed_manager, caregiver_manager, delete_bed, delete_patient, edit_bed,edit_caregiver, edit_patient, patient_manager
from lineIntegrations.views import linebot, verify, order, medicament, notify

urlpatterns = [
    path('', index),
    path('index', index, name='index'),
    path('admin', admin.site.urls),
    path('login', login_view, name='login'),
    path('logout', logout_view, name='logout'),
    path('creat_account/', register, name='creat_account'),
    path('caregiver_manager/',caregiver_manager, name='caregiver_manager'),
    path('caregivers/edit/<int:caregiver_id>/', edit_caregiver, name='edit_caregiver'), 
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('patient_manager/', patient_manager, name='patient_manager'),
    path('add_patient/', add_patient, name='add_patient'),
    path('edit_patient/<int:patient_id>/', edit_patient, name='edit_patient'),
    path('delete_patient/<int:patient_id>/', delete_patient, name='delete_patient'),
    path('bed_manager/', bed_manager, name='bed_manager'),
    path('bed_manager/add/', add_bed, name='add_bed'),
    path('bed_manager/edit/<int:bed_id>/', edit_bed, name='edit_bed'),
    path('bed_manager/delete/<int:bed_id>/', delete_bed, name='delete_bed'),
    path('suppliers/', supplier_list, name='suppliers'),
    path('suppliers/add/', add_supplier, name='add_supplier'),
    path('suppliers/edit/<int:supplier_id>/', edit_supplier, name='edit_supplier'),
    path('suppliers/delete/<int:supplier_id>/', delete_supplier, name='delete_supplier'),

    path('main_courses/', main_course_list, name='main_course'),
    path('main_courses/add/', add_main_course, name='add_main_course'),
    path('main_courses/edit/<int:course_id>/', edit_main_course, name='edit_main_course'),
    path('main_courses/delete/<int:course_id>/', delete_main_course, name='delete_main_course'),


    path('purchase_details/', purchase_detail_list, name='purchase_detail'),
    path('purchase_details/create/', purchase_detail_create, name='purchase_detail_create'),
    path('purchase_details/update/<int:pk>/', purchase_detail_update, name='purchase_detail_update'),
    path('purchase_details/delete/<int:pk>/', purchase_detail_delete, name='purchase_detail_delete'),

    path('bom_settings/', main_course_bom_settings, name='bom_settings'),


    path('edit_course_sides/<int:pk>/', edit_course_sides, name='edit_course_sides'),
    path('delete_course_sides/<int:pk>/', delete_course_sides, name='delete_course_sides'),
    path('inventory_management/', inventory_management, name='inventory_management'),
    # path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    

    path('course_order/', main_course_bom_settings, name='course_order'), #餐點配送管理
    path('medicine_order/', main_course_bom_settings, name='medicine_order'), #藥物配送管理


    path('linebot', linebot.line_bot_webhook),
    path('linebot/verify', verify.getWebPage),
    path('linebot/order', order.getWebPage),
    path('linebot/medicament', medicament.getWebPage),
    path('linebot/notify', notify.getWebPage),
    path('linebot/api/notifyList', notify.getPatientNotifyList)



    # path('add_purchase/', add_purchase, name='add_purchase'),
    # path('add_medicine/', add_medicine, name='add_medicine'),
    # path('medicine_list/', medicine_list, name='medicine_list'), 
    # path('modify_medicine/<int:medicine_id>/', modify_medicine, name='modify_medicine'),
    # path('delete_medicine/<int:medicine_id>/', delete_medicine, name='delete_medicine'),
    # path('warehouse/', warehouse_view, name='warehouse'),
    # path('warehouses/toggle/<int:warehouse_id>/', toggle_active, name='toggle_active'),
    # path('warehouse/delete/<int:warehouse_id>/', delete_warehouse, name='delete_warehouse'),
    # path('purchase/delete/<int:order_id>/', delete_purchase, name='delete_purchase'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
