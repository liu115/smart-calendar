from rest_framework import serializers
from app.models import Event

class CalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        # fields = '__all__'
        fields = ('id', 'comment', 'last_modify_date', 'created')
