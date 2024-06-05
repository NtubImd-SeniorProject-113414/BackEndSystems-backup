from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from backendApp.decorator import group_required
from backendApp.forms import RfidCardForm
from backendApp.middleware import login_required
from django.core.paginator import Paginator
from django.utils import timezone
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from ..models import RfidCard
from ..module import mqtt
import json
from django.http import JsonResponse

@group_required('caregiver')
@login_required
def card_list(request):
    query = request.GET.get('query', '')
    if query:
        cards = RfidCard.objects.filter(RfidCard_code__icontains=query)
    else:
        cards = RfidCard.objects.all().order_by('created_time')
    
    paginator = Paginator(cards, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'card/card_manager.html', {'page_obj': page_obj, 'query': query})

@group_required('caregiver')
@login_required
def call_card_sensor(request):
    if request.method == 'POST':
        mqtt.send_mqtt_message('addCard', topic='ntubimd/registerCard')
    return redirect('card_manager')

# @group_required('caregiver')
# @login_required
def add_card(request):
    try:
        card_code = str(request.body).replace("'","").replace("b","")
        print(card_code)
        if card_code:
            RfidCard.objects.create(rfidCard_code=card_code)
            return HttpResponse("新增成功")
    except Exception as e: 
        return HttpResponse("卡號已存在")




@group_required('caregiver')
@login_required
def edit_card(request, card_code):
    card = get_object_or_404(RfidCard, rfidCard_code=card_code)
    if request.method == 'POST':
        form = RfidCardForm(request.POST, instance=card)
        if form.is_valid():
            form.save()  
            return redirect('card_manager')
    else:
        form = RfidCardForm(instance=card)
    
    return render(request, 'card/edit_card.html', {'form': form})

@group_required('caregiver')
@login_required
def delete_card(request, card_code):
    card = get_object_or_404(RfidCard, rfidCard_code=card_code)
    card.delete()
    return redirect('card_manager')