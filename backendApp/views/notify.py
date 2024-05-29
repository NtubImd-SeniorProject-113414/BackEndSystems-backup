from datetime import datetime
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q
from backendApp.decorator import group_required
from backendApp.middleware import login_required
from ..models import Notify, Patient, PatientNotifys
from ..forms import NotifyForm


@login_required
@group_required('caregiver')
def send_notify(request):
    if request.method == 'POST':
        form = NotifyForm(request.POST)
        if form.is_valid():
            try:
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
                notify_id = notify.notify_id
                form = NotifyForm()
                return render(request, 'notify/send_notify.html', {'form': form, 'message': "訊息發送成功", "css": "alert alert-success", "notify_id": notify_id})
            except:
                return render(request, 'notify/send_notify.html', {'form': form, 'message': "訊息發送失敗", "css": "alert alert-danger"})
    else:
        form = NotifyForm()
    return render(request, 'notify/send_notify.html', {'form': form})

@login_required
def edit_notify(request, notify_id):
    notify = get_object_or_404(Notify, notify_id=notify_id)
    if request.method == 'POST':
        form = NotifyForm(request.POST, instance=notify)
        if form.is_valid():
            try:
                form.save()
                patients = form.cleaned_data['patients']
                notify.patientnotifys_set.all().delete()
                for patient in patients:
                    PatientNotifys.objects.create(
                        notify=notify,
                        patient=patient,
                        is_read=False
                    )  
                return render(request, 'notify/edit_notify.html', {'message': "訊息編輯成功", "css": "alert alert-success", 'form': form})
            except:
                return render(request, 'notify/edit_notify.html', {'message': "訊息編輯失敗", "css": "alert alert-danger", 'form': form})
    else:
        associated_patients = Patient.objects.filter(patientnotifys__notify=notify)
        form = NotifyForm(instance=notify, initial={'patients': associated_patients})
    return render(request, 'notify/edit_notify.html', {'form': form})


@group_required('caregiver')
@login_required
def delete_notify(request, notify_id):
    notify = get_object_or_404(Notify, notify_id=notify_id)
    notify.delete()
    return redirect('notify_manager')

@login_required
@group_required('caregiver')
def notify_manager(request):
    notifys = Notify.objects.all().order_by('-created_time')
    patients = Patient.objects.all()

    query = request.GET.get('text')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    patient_id = request.GET.get('patient')

    if query:
        notifys = notifys.filter(Q(notify_message__icontains=query))
    if start_date:
        notifys = notifys.filter(created_time__gte=datetime.strptime(start_date, '%Y-%m-%d'))
    if end_date:
        notifys = notifys.filter(created_time__lte=datetime.strptime(end_date, '%Y-%m-%d'))
    if patient_id:
        notifys = notifys.filter(patientnotifys__patient_id=patient_id)

    paginator = Paginator(notifys, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'notify/notify_manager.html', {'page_obj': page_obj, 'patients': patients})