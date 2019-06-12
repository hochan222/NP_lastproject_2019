from rest_framework import serializers
from .models import Post_rssi


class rssiSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'data',
        )
        model = Post_rssi
