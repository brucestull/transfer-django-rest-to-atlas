from rest_framework import serializers

from accounts.models import CustomUser


class CustomUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'username',
            'url',
            'email',
            'first_name',
            'last_name',
        ]
