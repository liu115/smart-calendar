from rest_framework import serializers
from app.models import Calendar

class CalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calendar
        # fields = '__all__'
        fields = ('id', 'comment', 'last_modify_date', 'created')
