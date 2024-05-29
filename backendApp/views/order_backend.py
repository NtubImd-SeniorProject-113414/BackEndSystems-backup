from django.shortcuts import render, redirect, get_object_or_404
from backendApp.decorator import group_required
from backendApp.forms import RfidCardForm
from backendApp.middleware import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from datetime import datetime

from ..models import Order, MealOrderTimeSlot, RfidCard, OrderState
from ..module import mqtt

@login_required
@group_required('caregiver')
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
        'current_time_period': mealTime
    })
    
@login_required
@group_required('caregiver')
def order_list_history(request):
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
@group_required('caregiver')
def delivery_order(request, card_code):
    if request.method == 'POST':
        mqtt.send_mqtt_message(card_code, topic='/delivery/order')
    return redirect('order_delivery_management')

# 當車送達且拿取後 => 發mqtt給nodeRed => 發此API 改狀態
@login_required
@group_required('caregiver')
def finish_order(request, card_code):
    patient_id = get_object_or_404(RfidCard, pk=card_code).patient_id
    order = Order.objects.filter(patient_id=patient_id).order_by('order_time').first()
    arrived_state = get_object_or_404(OrderState, pk=3)
    order.orderState = arrived_state
    order.save()

@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    canceled_state = get_object_or_404(OrderState, pk=4)
    order.orderState = canceled_state
    order.save()
    return redirect('order_delivery_management')

