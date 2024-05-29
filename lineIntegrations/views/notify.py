from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from backendApp.models import PatientNotifys
from backendApp.middleware import line_verify
from django.utils.dateformat import format


@csrf_exempt
@line_verify
def getWebPage(request, *args, **kwargs):
    return render(request, 'notify.html')

@csrf_exempt
@line_verify
def getPatientNotifyList(request, *args, **kwargs):
    patient_id = kwargs.get('patient_id')
    notifys = PatientNotifys.objects.filter(patient_id=patient_id).select_related('notify').order_by('-notify__created_time')
    notify_list = []
    for pn in notifys:
        notify_list.append({
            'notify_id': pn.notify.notify_id,
            'notify_message': pn.notify.notify_message,
            'created_time': format(pn.notify.created_time, 'Y年m月d日 H時i分'),
            'is_read': pn.is_read
        })
    return JsonResponse({'notifys': notify_list}, status=200)

@csrf_exempt
@line_verify
def userReadNotify(request, *args, **kwargs):
    patient_id = kwargs.get('patient_id')
    if request.method == 'POST':
        notify_id = request.POST.get('notify_id')
        if notify_id and patient_id:
            notify = get_object_or_404(PatientNotifys, notify_id=notify_id, patient_id=patient_id)
            notify.is_read = True
            notify.save()
            return JsonResponse({'status': '成功'})
    return JsonResponse({'status': 'error', 'message': '失敗'}, status=405)