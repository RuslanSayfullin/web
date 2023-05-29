from rest_framework import serializers
from django.contrib.auth.models import User
from apps.froze.models import Froze


class FrozeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Froze
        fields = ('uuid', 'name', 'address', 'phone', 'owner', 'type_production', )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        return user