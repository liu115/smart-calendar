from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from app.models import Calendar, User
from app.serializers import CalendarSerializer

from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

class CalendarViewSet(viewsets.ModelViewSet):
    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer

def login(request):
    pass

def register(request):
    
    if request.method == 'GET':
        return render(request, 'register.html')
    elif request.method == 'POST':
        context = {
            "name": request.POST['name'],
            "password": request.POST['password']
        }
        new_user = User.objects.create()
        new_user.name = request.POST['name']
        new_user.password = request.POST['password']
        new_user.save()
        return render(request, 'register.html', context)
