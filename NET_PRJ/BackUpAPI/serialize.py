from rest_framework import serializers
from .models import BU_model

class BU_ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BU_model
        fields = '__all__'