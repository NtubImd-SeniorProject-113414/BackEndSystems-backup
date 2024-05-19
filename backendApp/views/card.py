from django.shortcuts import render, redirect, get_object_or_404
from backendApp.decorator import group_required
from backendApp.forms import RfidCardForm
from backendApp.middleware import login_required
from django.core.paginator import Paginator

from ..models import RfidCard
from ..module import mqtt
@group_required('admin')
@login_required
def card_list(request):
    query = request.GET.get('query', '')

    if query:
        cards = RfidCard.objects.filter(RfidCard_code__icontains=query)
    else:
        cards = RfidCard.objects.all().order_by('created_time')
    print(cards)
    paginator = Paginator(cards, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'card/card_manager.html', {'page_obj': page_obj, 'query': query})

@group_required('admin')
@login_required
def add_card(request):
    if request.method == 'POST':
        mqtt.send_mqtt_message('signup', topic='/signup')
    return redirect('card/card_manager.html')

@group_required('admin')
@login_required
def delete_card(request, card_code):
    card = get_object_or_404(RfidCard, RfidCard_code=card_code)
    card.delete()
    return redirect('card/card_manager.html')

@group_required('admin')
@login_required
def edit_card(request, card_code):
    card = get_object_or_404(RfidCard, RfidCard_code=card_code)
    card.delete()
    return redirect('card/card_manager.html')