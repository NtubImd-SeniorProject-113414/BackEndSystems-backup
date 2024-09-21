from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

from backendApp.decorator import group_required
from backendApp.forms import SelectorForm
from backendApp.form_list.turn_point import TurnPointForm
from backendApp.middleware import login_required
from backendApp.models import RouteCondition, TurnPoint
from backendApp.module.pointPrint import create_point_pdf

@login_required
@group_required('caregiver')
def stop_point(request):
    if request.method == 'POST':
        form = SelectorForm(request.POST)
        if form.is_valid():
            patients = form.cleaned_data['patients']
            data_list = [[f"{str(patient.patient_id)} : {str(patient.patient_name)}", settings.MEDIA_ROOT + "/" + patient.patient_qr_point.qr_code_image] for patient in patients]
            pdf_data = create_point_pdf(data_list)

            # 設置 response 的 Content-Type 和 Content-Disposition 來讓 PDF 自動下載
            response = HttpResponse(pdf_data, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="stop_point_report.pdf"'
            return response
        else:
            print("表單驗證失敗：", form.errors)
    form = SelectorForm()
    return render(request, 'robotManagement/stop_point.html', {'form': form})

@login_required
@group_required('caregiver')
def turn_point(request):
    turn_points = TurnPoint.objects.all()

    turn_points_with_forms = [
        {
            'turn_point': turn_point, 
            'form': TurnPointForm(
                instance=turn_point
            )
        }
        for turn_point in turn_points
    ]

    return render(request, 'robotManagement/turn_point.html', {
        'add_form': TurnPointForm(),
        'turn_points_with_forms': turn_points_with_forms
    })


@group_required('caregiver')
@login_required
def add_turn_point(request):
    if request.method == 'POST':
        form = TurnPointForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '事件新增成功。')
            return redirect('turn_point_manager')
    else:
        form = TurnPointForm()

    return render(request, 'robotManagement/turn_point.html', {
        'add_form': form,
    })

@group_required('caregiver')
@login_required
def edit_turn_point(request, turn_point_id):
    turn_point = get_object_or_404(TurnPoint, turn_point_id=turn_point_id)
    if request.method == 'POST':
        form = TurnPointForm(request.POST, instance=turn_point)
        if form.is_valid():
            form.save()
            messages.success(request, '事件資訊更新成功。')
            return redirect('turn_point_manager')
    else:
        form = TurnPointForm(instance=turn_point)

    return render(request, 'robotManagement/edit_turn_point.html', {
        'edit_form': form,
        'turn_point': turn_point
    })

@group_required('caregiver')
@login_required
def delete_turn_point(request, turn_point_id):
    turn_point = get_object_or_404(TurnPoint, turn_point_id=turn_point_id)
    turn_point.delete()
    messages.success(request, '事件已刪除。')
    return redirect('turn_point_manager')