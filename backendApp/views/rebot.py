from django.shortcuts import render

def robot_main(request):
    return render(request, 'robot/main.html')
