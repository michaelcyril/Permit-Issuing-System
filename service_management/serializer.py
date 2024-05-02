from rest_framework import serializers
from .models import *


class PermitPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permit
        fields = [
            'customer',
            'livestock_number',
            'permit_typec',
        ]


class PermitGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permit
        fields = '__all__'
        depth = 2

