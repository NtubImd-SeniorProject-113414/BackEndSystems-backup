from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from django.contrib import admin
from backendApp.views.notify import edit_notify, notify_manager, send_notify, delete_notify
from backendApp.views.order_timeSlot import timeSlots_manager, create_timeSlot, edit_timeSlot, delete_timeSlot
from backendApp.views.views import index, edit_profile
from backendApp.login import login_view,logout_view
from backendApp.caresystem_views import *
from backendApp.views import userManagement, card, order_backend, medicine
from lineIntegrations.views import linebot, verify, order, medicament, notify

urlpatterns = [
    path('', index),
    path('index', index, name='index'),
    path('admin', admin.site.urls),
    path('login', login_view, name='login'),
    path('logout', logout_view, name='logout'),
    path('user_manager/',userManagement.user_manager, name='user_manager'),
    path('user_manager/create', userManagement.create_user, name='add_user'),
    path('user_manager/edit/<int:user_id>/', userManagement.edit_user, name='edit_user'),
    
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
    
    path('notify_manager', notify_manager, name='notify_manager'),
    path('notify_manager/send', send_notify, name='send_notify'),
    path('notify_manager/edit/<int:notify_id>/', edit_notify, name='edit_notify'),
    path('notify_manager/delete/<int:notify_id>/', delete_notify, name='delete_notify'),

    path('timeslot_manager', timeSlots_manager, name='timeslot_manager'),
    path('timeslot_manager/add', create_timeSlot, name='create_timeSlot'),
    path('timeslot_manager/edit/<int:time_slot_id>/', edit_timeSlot, name='update_timeSlot'),
    path('timeslot_manager/delete/<int:time_slot_id>/', delete_timeSlot, name='delete_timeSlot'),



    path('linebot', linebot.line_bot_webhook),
    path('linebot/verify', verify.getWebPage),
    path('linebot/order', order.getWebPage),
    path('linebot/medicament', medicament.getWebPage),
    path('linebot/notify', notify.getWebPage),
    path('linebot/api/readNotify', notify.userReadNotify, name='userReadNotify'),
    path('linebot/api/notifyList', notify.getPatientNotifyList, name='userNotifyList'),


    # path('add_purchase/', add_purchase, name='add_purchase'),
    # path('add_medicine/', add_medicine, name='add_medicine'),
    # path('medicine_list/', medicine_list, name='medicine_list'), 
    # path('modify_medicine/<int:medicine_id>/', modify_medicine, name='modify_medicine'),
    # path('delete_medicine/<int:medicine_id>/', delete_medicine, name='delete_medicine'),
    # path('warehouse/', warehouse_view, name='warehouse'),
    # path('warehouses/toggle/<int:warehouse_id>/', toggle_active, name='toggle_active'),
    # path('warehouse/delete/<int:warehouse_id>/', delete_warehouse, name='delete_warehouse'),
    # path('purchase/delete/<int:order_id>/', delete_purchase, name='delete_purchase'),

    path('card_manager/', card.card_list, name='card_manager'),
    path('card_manager/call_sensor', card.call_card_sensor, name='call_sensor'),
    # for nodeRed
    path('card_manager/add', card.add_card, name='add_card'),
    path('card_manager/edit/<str:card_code>', card.edit_card, name='edit_card'),
    path('card_manager/delete_card/<str:card_code>', card.delete_card, name='delete_card'),
    
    path('order_delivery_management/', order_backend.order_list, name='order_delivery_management'),
    path('order_delivery_management/history', order_backend.order_list_history, name='history'),
    path('order_deliver_management/delivery/<str:card_code>', order_backend.delivery_order, name='delivery_order'),
    path('order_deliver_management/cancel/<int:order_id>', order_backend.cancel_order, name='cancel_order'),
    # for nodeRed
    path('order_deliver_management/finish/<str:card_code>', order_backend.finish_order, name='finish_order'),
    
    path('medicine_order_management_review/', medicine.medicine_review_list, name='medicine_order_management_review'), 
    path('medicine_order_management_delivery/', medicine.medicine_delivery_list, name='medicine_order_management_delivery'), 
    path('medicine_order_management_history/', medicine.medicine_history_list, name='medicine_order_management_history'),
    path('medicine_order_management/accept/<int:medicineDemand_id>', medicine.accept_medicine_demand, name='accept_medicine'), 
    path('medicine_order_management/reject/<int:medicineDemand_id>', medicine.reject_medicine_demand, name='reject_medicine'), 
    path('medicine_order_management/cancel/<int:medicineDemand_id>', medicine.cancel_medicine_demand, name='cancel_medicine'), 
    path('medicine_order_management/delivery/<int:medicineDemand_id>', medicine.delivery_medicine, name='delivery_medicine'),
    
    # for nodeRed
    path('medicine_order_management/finish/<str:card_code>', medicine.finish_medicine_demand, name='finish_medicine_order'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
