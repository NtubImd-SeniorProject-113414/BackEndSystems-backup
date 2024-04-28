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
from backendApp.views import delete_warehouse, index, add_medicine, medicine_list,delete_medicine,modify_medicine,add_purchase,\
    warehouse_view,toggle_active,delete_purchase,edit_profile
from backendApp.login import login_view,logout_view
from backendApp.account import register
from backendApp.caresystem_views import add_bed, add_patient, bed_manager, caregiver_manager, delete_bed, delete_patient, edit_bed,edit_caregiver, edit_patient, patient_manager

from backendApp.caresystem_views import add_patient, caregiver_manager, delete_patient,edit_caregiver, edit_patient, patient_manager
from django.contrib.auth import views as auth_views

from lineIntegrations.views import linebot, verify

urlpatterns = [
    path('', index, name='index'),
    path('admin', admin.site.urls),
    path('login', login_view, name='login'),
    path('logout', logout_view, name='logout'),
    path('add_purchase/', add_purchase, name='add_purchase'),
    path('add_medicine/', add_medicine, name='add_medicine'),
    path('medicine_list/', medicine_list, name='medicine_list'), 
    path('modify_medicine/<int:medicine_id>/', modify_medicine, name='modify_medicine'),
    path('delete_medicine/<int:medicine_id>/', delete_medicine, name='delete_medicine'),
    path('warehouse/', warehouse_view, name='warehouse'),
    path('warehouses/toggle/<int:warehouse_id>/', toggle_active, name='toggle_active'),
    path('warehouse/delete/<int:warehouse_id>/', delete_warehouse, name='delete_warehouse'),
    path('purchase/delete/<int:order_id>/', delete_purchase, name='delete_purchase'),
    path('creat_account/', register, name='creat_account'),
    path('caregiver_manager/',caregiver_manager, name='caregiver_manager'),
    path('caregivers/edit/<int:caregiver_id>/', edit_caregiver, name='edit_caregiver'), 
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('patient_manager/', patient_manager, name='patient_manager'),
    path('add_patient/', add_patient, name='add_patient'),
    path('edit_patient/<int:patient_id>/', edit_patient, name='edit_patient'),
    path('delete_patient/<int:patient_id>/', delete_patient, name='delete_patient'),
    path('beds/', bed_manager, name='bed_manager'),
    path('beds/add/', add_bed, name='add_bed'),
    path('beds/edit/<int:bed_id>/', edit_bed, name='edit_bed'),
    path('beds/delete/<int:bed_id>/', delete_bed, name='delete_bed'),
    # path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    

    path('linebot', linebot.line_bot_webhook),
    path('linebot/verify', verify.getWebPage)

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
