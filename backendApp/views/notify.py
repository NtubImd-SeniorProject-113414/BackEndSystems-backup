from django.shortcuts import render, redirect
from django.utils import timezone
from ..models import Notify
from ..forms import NotifyForm

def send_notification(request):
    if request.method == 'POST':
        form = NotifyForm(request.POST)
        if form.is_valid():
            notify_message = form.cleaned_data['notify_message']
            patients = form.cleaned_data['patients']

            for patient in patients:
                Notify.objects.create(
                    notify_message=notify_message,
                    patient=patient,
                    created_time=timezone.now()
                )
            form = NotifyForm()
            return render(request, 'notify/send_message.html', {'message': "訊息發送成功", "css": "alert alert-success", 'form': form})
    else:
        form = NotifyForm()
    return render(request, 'notify/send_message.html', {'form': form})
