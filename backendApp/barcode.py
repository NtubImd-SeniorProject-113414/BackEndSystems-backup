from django.http import JsonResponse
from .models import Prescription

def get_prescription_by_barcode(request, barcode):
    try:
        prescription = Prescription.objects.get(barcode=barcode)
        response_data = {
            "date": prescription.date,
            "medicines": list(prescription.medicines.values('medicine_name', 'dosage', 'dispensing_q'))
        }
        return JsonResponse(response_data, safe=False)
    except Prescription.DoesNotExist:
        return JsonResponse({'error': 'Prescription not found'}, status=404)