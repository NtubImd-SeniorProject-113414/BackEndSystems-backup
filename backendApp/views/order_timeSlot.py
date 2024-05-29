from datetime import datetime
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q
from backendApp.decorator import group_required
from backendApp.middleware import login_required
from ..models import MealOrderTimeSlot
from ..forms import MealOrderTimeSlotForm

@login_required
@group_required('caregiver')
def timeSlots_manager(request):
    timeSlots = MealOrderTimeSlot.objects.all()
    return render(request, 'orderTimeSlot/timeslot_manager.html', {'timeSlots': timeSlots})

@login_required
@group_required('caregiver')
def create_timeSlot(request):
    message = ""
    css_class = "alert alert-success"
    if request.method == 'POST':
        form = MealOrderTimeSlotForm(request.POST)
        if form.is_valid():
            time_slot = form.save()
            form = MealOrderTimeSlotForm()
            message = f"時段創建成功"
            return render(request, 'orderTimeSlot/add_timeslot.html', {
                'form': form,
                'message': message,
                'timeSlot_id': time_slot.timeSlot_id,
                'css': css_class
            })
        else:
            message = "創建失敗，請修正以下的錯誤"
            css_class = "alert alert-danger"
            return render(request, 'orderTimeSlot/add_timeslot.html', {
                'form': form,
                'message': message,
                'css': css_class
            })

    else:
        form = MealOrderTimeSlotForm()
        return render(request, 'orderTimeSlot/add_timeslot.html', {
            'form': form
        })

@login_required
@group_required('caregiver')
def edit_timeSlot(request, time_slot_id):
    message = ""
    css_class = "alert alert-success"
    time_slot = get_object_or_404(MealOrderTimeSlot, pk=time_slot_id)

    if request.method == 'POST':
        form = MealOrderTimeSlotForm(request.POST, instance=time_slot)
        if form.is_valid():
            form.save()
            message = f"時段更新成功"
            return render(request, 'orderTimeSlot/edit_timeslot.html', {
                'form': form,
                'message': message,
                'css': css_class
            })
        else:
            message = "更新失敗，請修正以下的錯誤"
            css_class = "alert alert-danger"
            return render(request, 'orderTimeSlot/edit_timeslot.html', {
                'form': form,
                'message': message,
                'css': css_class
            })

    else:
        form = MealOrderTimeSlotForm(instance=time_slot)
        return render(request, 'orderTimeSlot/edit_timeslot.html', {
            'form': form
        })

@login_required
@group_required('caregiver')
def delete_timeSlot(request, time_slot_id):
    timeSlot = get_object_or_404(MealOrderTimeSlot, timeSlot_id=time_slot_id)
    timeSlot.delete()
    return redirect('timeslot_manager')