from django.shortcuts import render
from django.utils import timezone
from ..models import Notify, PatientNotifys
from ..forms import NotifyForm

def send_notification(request):
    if request.method == 'POST':
        form = NotifyForm(request.POST)
        if form.is_valid():
            notify_message = form.cleaned_data['notify_message']
            patients = form.cleaned_data['patients']
            notify = Notify.objects.create(
                notify_message=notify_message,
                created_time=timezone.now()
            )
            for patient in patients:
                PatientNotifys.objects.create(
                    notify=notify,
                    patient=patient,
                    is_read=False
                )

            form = NotifyForm()
            return render(request, 'notify/send_message.html', {'message': "訊息發送成功", "css": "alert alert-success", 'form': form})
    else:
        form = NotifyForm()
    return render(request, 'notify/send_message.html', {'form': form})
