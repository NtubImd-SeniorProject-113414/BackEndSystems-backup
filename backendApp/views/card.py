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
        mqtt.send_mqtt_message('addCard', topic='registerCard')
    return redirect('card_manager')

@group_required('caregiver')
@login_required
def add_card(request):
    if request.method == 'POST':
        # 从 POST 数据中获取 card_code
        card_code = request.POST.get('card_code')
        if card_code:  # 检查 card_code 是否存在
            create_time = timezone.now()
            RfidCard.objects.create(card_code=card_code, create_time=create_time)
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "card_updates_group",
                {
                    "type": "card.message",
                    "message": "新卡片已添加"
                }
            )
            return HttpResponse("OK")
        else:
            return HttpResponse("Card code is missing", status=400)
    return HttpResponse("Invalid request", status=405)

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
    card = get_object_or_404(RfidCard, RfidCard_code=card_code)
    card.delete()
    return redirect('card_manager')