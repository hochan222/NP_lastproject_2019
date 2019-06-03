from rest_framework import serializers
from .models import Post, Bachelor_data, IoT_data, IoT_home


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'title',
            'content',
        )
        model = Post


class BachelorSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'number',
            'data',
        )
        model = Bachelor_data

class IoTSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id',
            'state',
        )
        model = IoT_data

class IoThomeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'time',
            'temperature',
            'humidity'
        )
        model = IoT_home