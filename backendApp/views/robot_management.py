from django.shortcuts import render

from backendApp.forms import SelectorForm
from backendApp.models import Patient


def stop_point(request):
    form = SelectorForm()
    return render(request, 'robotManagement/stop_point.html', {'form': form})