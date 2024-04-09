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
from backendApp.views import delete_warehouse, index, add_medicine, medicine_list,delete_medicine,modify_medicine,add_purchase,warehouse_view,toggle_active,delete_purchase
from backendApp.login import login_view,logout_view

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

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
