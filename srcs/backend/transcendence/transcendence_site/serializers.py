from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import MyUser

class UserSerializer(serializers.ModelSerializer):

    friends = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=MyUser.objects.all(),
        required=False
    )
    
    class Meta:
        model = MyUser
        fields = ['id', 'username', 'email', 'profile_picture', 'password', 'friends']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)