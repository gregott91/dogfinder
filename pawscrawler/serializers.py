from .models import Pet
from rest_framework import serializers


class PetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Pet
        fields = ['id', 'status']