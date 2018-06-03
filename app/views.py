from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from app.models import Calendar
from app.serializers import CalendarSerializer

from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
def index(request):
    template = loader.get_template('index.html')
    return render(request, 'index.html')

class CalendarViewSet(viewsets.ModelViewSet):
    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer

