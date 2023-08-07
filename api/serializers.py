from rest_framework import serializers
from .models import StoreStatus, StoreHours, StoreTimezone

class StoreStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreStatus
        fields = '__all__'

class StoreHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreHours
        fields = '__all__'

class StoreTimezoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreTimezone
        fields = '__all__'
