from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render

from backendApp.decorator import group_required
from backendApp.forms import SelectorForm
from backendApp.middleware import login_required
from backendApp.models import Patient
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