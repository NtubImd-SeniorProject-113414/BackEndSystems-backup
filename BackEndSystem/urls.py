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
from django.contrib import admin
from django.urls import path
from backendApp.views import index, add_medicine, medicine_list, show_stock, warehouse_list, toggle_warehouse_status, delete_medicine

urlpatterns = [
    path('admin/', admin.site.urls),  # Import admin module from django.contrib
    path('', index, name='index'),
    path('add_medicine/', add_medicine, name='add_medicine'),
    path('medicine_list/', medicine_list, name='medicine_list'), 
    path('warehouse/', warehouse_list, name='warehouse_list'),
    path('toggle-warehouse-status/<int:warehouse_id>/', toggle_warehouse_status, name='toggle_warehouse_status'),
    path('delete_medicine/<int:medicine_id>/', delete_medicine, name='delete_medicine'),
    path('show_stock/', show_stock, name='show_stock'),

]