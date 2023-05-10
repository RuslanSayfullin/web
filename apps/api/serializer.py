from rest_framework import serializers

from apps.froze.models import Froze


class FrozeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Froze
        fields = ('uuid', 'name', 'address', 'phone', 'owner', 'type_production', )
