from django.shortcuts import render, redirect, get_object_or_404
from backendApp.decorator import group_required
from backendApp.forms import RfidCardForm
from backendApp.middleware import login_required
from django.core.paginator import Paginator
from django.db.models import Prefetch, Q
from django.utils import timezone
from datetime import datetime

from ..models import Order, OrderState, Bed, MealOrderTimeSlot
from ..module import mqtt

@login_required
def order_list(request):
    current_time = datetime.now().strftime('%H:%M')
    date = timezone.now().date()

    mealTime = MealOrderTimeSlot.find_time_slot(current_time)
    orders = Order.objects.filter(
        (Q(orderState__OrderState_code=1) | Q(orderState__OrderState_code=2)) &
        Q(order_time__date=date)
    )
    for order in orders:
        order.first_bed_number = order.patient.bed_set.first().bed_number if order.patient.bed_set.exists() else "未分配"


    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'order/order_delivery_management.html', {
        'page_obj': page_obj,
        'current_time_period': mealTime  # 将当前时段状态传递到模板
    })
    
@login_required
def order_list_history(request):
    current_time = datetime.now().strftime('%H:%M')
    date = timezone.now().date()

    mealTime = MealOrderTimeSlot.find_time_slot(current_time)
    orders = Order.objects.filter(
        (Q(orderState__OrderState_code=3) | Q(orderState__OrderState_code=4))
    )
    for order in orders:
        order.first_bed_number = order.patient.bed_set.first().bed_number if order.patient.bed_set.exists() else "未分配"


    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'order/order_delivery_management_history.html', {'page_obj': page_obj,})

@login_required
def delivery_order(request, card_code):
    if request.method == 'POST':
        mqtt.send_mqtt_message(card_code, topic='/delivery')
    return redirect('order_delivery_management')

@login_required
def cancel_order(request, order_id):
    return redirect('order_delivery_management')

@login_required
def finish_order(request, order_id):
    return redirect('order_delivery_management')