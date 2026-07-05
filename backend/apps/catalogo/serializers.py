from rest_framework import serializers
from .models import Barbie, BarbieImage

class BarbieImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BarbieImage
        fields = ['id', 'barbie', 'image', 'is_primary', 'uploaded_at']

class BarbieSerializer(serializers.ModelSerializer):
    images = BarbieImageSerializer(many=True, read_only=True)

    class Meta:
        model = Barbie
        fields = '__all__'
