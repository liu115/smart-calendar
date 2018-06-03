from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from app.models import Calendar
from app.serializers import CalendarSerializer

class CalendarViewSet(viewsets.ModelViewSet):
    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer

