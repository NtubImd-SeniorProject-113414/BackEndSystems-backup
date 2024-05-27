from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from datetime import datetime
from backendApp.models import MainCourse, MealOrderTimeSlot, OrderState, Patient, Order
from backendApp.middleware import line_verify
from lineIntegrations.module.lineVerify import getLineUserUidByToken


@csrf_exempt
@line_verify
def getWebPage(request):
    nowTime = datetime.now()
    formatted_time = nowTime.strftime("%H:%M")
    #formatted_time = "19:31" #測試用
    nowTimeSlot = MealOrderTimeSlot.find_time_slot(formatted_time)
    nextTimeSlot = MealOrderTimeSlot.find_nearest_time_slot(nowTimeSlot, formatted_time)
    next_time_slot_str = f"{nextTimeSlot.startTime.strftime('%H:%M')} 至 {nextTimeSlot.deadlineTime.strftime('%H:%M')}"

    access_token = request.session.get('line_access_token')
    LineUid = getLineUserUidByToken(access_token)
    patient_id = Patient.getpatientIdByLineUid(LineUid)

    #這時段是否點餐了
    if nowTimeSlot!= None:
        orderData = Order.getOrderByPatientIdAndTimeSlot(patient_id, nowTimeSlot)
        if orderData:
            return render(request, 'order/state.html', {'orderData': orderData[0], 'nextTimeSlotName': nextTimeSlot.timeSlot_name, 'nextTimeSlot': next_time_slot_str})

    #時段檢查
    if (nowTimeSlot is None) or (formatted_time > nowTimeSlot.deadlineTime.strftime('%H:%M')):
        if nowTimeSlot is None:
            msg = '目前尚未開放點餐'
        else:
            msg = '本時段點餐時間已過'
        return render(request, 'order/unopened.html', {'msg': msg, 'nextTimeSlotName': nextTimeSlot.timeSlot_name, 'nextTimeSlot': next_time_slot_str})

    if request.method == 'GET':
        courses = MainCourse.objects.filter(timeSlot=nowTimeSlot)
        return render(request, 'order/menu.html', {'timeSlotName': nowTimeSlot.timeSlot_name, 'courses': courses})
    elif request.method == 'POST':
        course_id = request.POST.get('courseId')
        defaultState = OrderState.objects.get(OrderState_code=1)
        order = Order.objects.create(patient_id=patient_id, course_id=course_id, order_quantity=1, orderState=defaultState)
        order.save()

        return JsonResponse({'message': '訂單已成功提交'}, status=201)
    
    return HttpResponse("Unsupported HTTP method", status=405)




