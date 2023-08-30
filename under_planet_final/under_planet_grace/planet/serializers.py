from rest_framework import serializers

from .models import *

class PlanetDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanetData
        fields = '__all__'