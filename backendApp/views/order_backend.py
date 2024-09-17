from django.shortcuts import render, redirect, get_object_or_404
from backendApp.decorator import group_required
from backendApp.middleware import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from datetime import datetime

from ..models import Order, MealOrderTimeSlot, OrderState, Vehicle, DeliveryAssignment, DeliveryStatus
from ..module import mqtt

@login_required
@group_required('caregiver')
def order_list(request):
    current_time = datetime.now().strftime('%H:%M')
    date = timezone.now().date()

    mealTime = MealOrderTimeSlot.find_time_slot(current_time)
    orders = Order.objects.filter(
        (Q(order_state__order_state_code=1) | Q(order_state__order_state_code=2)) &
        Q(order_time__date=date)
    )
    
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
        (Q(order_state__order_state_code=3) | Q(order_state__order_state_code=4))
    )
    print(orders[0].order_state.order_state_code)

    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'order/order_delivery_management_history.html', {'page_obj': page_obj,})

@login_required
@group_required('caregiver')
def deliver_orders(request):
    if request.method == 'POST':
        robot_id = request.POST.get('robot_id')
        order_ids = request.POST.getlist('orders')
        s_count = 0
        vehicle = get_object_or_404(Vehicle, vehicle_id=robot_id)
        if vehicle==None or vehicle.vehicle_status.vehicle_status_code != 2:
            messages.error(request, '目前無法調用該運送機器人。')
        else:
            for order_id in order_ids:
                order = get_object_or_404(Order, order_id=order_id)
                if order != None and order.order_state.order_state_code == 1:
                    current_location = order.patient.patient_qr_point
                    delivery_status = get_object_or_404(DeliveryStatus, delivery_status_code=1)
                    DeliveryAssignment.objects.create(
                        order=order,
                        vehicle=vehicle,
                        current_location=current_location,
                        delivery_status=delivery_status
                    )
                    order.order_state = get_object_or_404(OrderState, order_state_code=2)
                    order.save()
                    messages.success(request, f'成功運送「{order_id}號」訂單 !')
                    s_count += 1
                else:
                    messages.error(request, f'「{order_id}號」訂單狀態無效，無法運送 !')
            if s_count > 0:
                mqtt.send_mqtt_message('forward', topic='robot/control')

    return redirect('order_delivery_management')

@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    canceled_state = get_object_or_404(OrderState, pk=4)
    order.order_state = canceled_state
    order.save()
    return redirect('order_delivery_management')

