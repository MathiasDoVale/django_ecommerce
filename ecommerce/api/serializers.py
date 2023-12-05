# Serializers define the API representation.
from rest_framework import serializers
from user.models import CustomUser


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'is_staff']