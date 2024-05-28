from django.shortcuts import render, redirect, get_object_or_404
from backendApp.decorator import group_required
from backendApp.forms import RfidCardForm
from backendApp.middleware import login_required
from django.core.paginator import Paginator
from django.db.models import Prefetch, Q
from django.utils import timezone
from datetime import datetime

from ..models import MedicineDemand, MedicineDemandState, RfidCard
from ..module import mqtt



@login_required
@group_required('caregiver')
def medicine_review_list(request):
    date = timezone.now().date()
    medicines = MedicineDemand.objects.filter(
        Q(medicineDemandState__medicineDemandState_code=1) &
        Q(created_time__date=date)
    )
    
    for medicine in medicines:
        medicine.first_bed_number = medicine.patient.bed_set.first().bed_number if medicine.patient.bed_set.exists() else "未分配"

    paginator = Paginator(medicines, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'medicine/order_management_review.html', {'page_obj': page_obj})
  

@login_required
@group_required('caregiver')
def medicine_delivery_list(request):
    date = timezone.now().date()
    medicines = MedicineDemand.objects.filter(
        (Q(medicineDemandState__medicineDemandState_code=2) | Q(medicineDemandState__medicineDemandState_code=3)) &
        Q(review_time__date=date)
    )
    
    for medicine in medicines:
        medicine.first_bed_number = medicine.patient.bed_set.first().bed_number if medicine.patient.bed_set.exists() else "未分配"


    paginator = Paginator(medicines, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'medicine/order_management_delivery.html', {'page_obj': page_obj,})

@login_required
@group_required('caregiver')
def medicine_history_list(request):
    medicines = MedicineDemand.objects.filter(
        (Q(MedicineDemandState__medicineDemandState_code=4) | Q(medicineDemandState__MedicineDemandState_code=5))
    )

    paginator = Paginator(medicines, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'medicine/order_management_history.html', {'page_obj': page_obj,})

@login_required
@group_required('caregiver')
def accept_medicine_demand(request, medicineDemand_id):
    medicineDemand = get_object_or_404(MedicineDemand, pk=medicineDemand_id)
    waitForDeliveryState = get_object_or_404(MedicineDemandState, pk=2)
    medicineDemand.medicineDemandState = waitForDeliveryState
    medicineDemand.review_time = timezone.now()
    medicineDemand.save()
    return redirect('medicine_order_review')

@group_required('caregiver')
@login_required
def reject_medicine_demand(request, medicineDemand_id):
    medicineDemand = get_object_or_404(MedicineDemand, pk=medicineDemand_id)
    reject_State = get_object_or_404(MedicineDemandState, pk=5)
    medicineDemand.medicineDemandState = reject_State
    medicineDemand.save()
    return redirect('medicine_order_review')

@group_required('caregiver')
@login_required
def cancel_medicine_demand(request, medicineDemand_id):
    medicineDemand = get_object_or_404(MedicineDemand, pk=medicineDemand_id)
    reject_State = get_object_or_404(MedicineDemandState, pk=5)
    medicineDemand.medicineDemandState = reject_State
    medicineDemand.save()
    return redirect('medicine_order_delivery')


@login_required
@group_required('caregiver')
def delivery_medicine(request, medicineDemand_id):
    medicineDemand = get_object_or_404(MedicineDemand, pk=medicineDemand_id)
    patient_id = medicineDemand.patient_id
    card = get_object_or_404(RfidCard, patient_id=patient_id)
    mqtt.send_mqtt_message(card.RfidCard_code, topic='/delivery/medicine')
    
    delivering_State = get_object_or_404(MedicineDemandState, pk=3)
    medicineDemand.medicineDemandState = delivering_State
    medicineDemand.save()
    return redirect('medicine_order_delivery')

# 當車送達且拿取後 => 發mqtt給nodeRed => 發此API 改狀態
@group_required('caregiver')
@login_required
def finish_medicine_demand(request, card_code):
    rfidCard = get_object_or_404(RfidCard, pk=card_code)
    patient_id = rfidCard.patient_id
    medicineDemand = MedicineDemand.objects.filter(patient_id=patient_id).order_by('review_time').first()
    arrived_state = get_object_or_404(MedicineDemandState, pk=4)
    medicineDemand.medicineDemandState = arrived_state
    medicineDemand.save()