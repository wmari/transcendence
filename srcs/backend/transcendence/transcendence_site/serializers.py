from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import MyUser
from django.contrib.auth import login, authenticate
from . import models

class UserSerializer(serializers.ModelSerializer):

    friends = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=MyUser.objects.all(),
        required=False
    )
    
    class Meta:
        model = MyUser
        fields = ['id', 'username', 'email', 'profil_picture', 'password', 'friends']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)



class OauthUserSerializer(serializers.Serializer): #recupere le login et l'email
      login = serializers.CharField()
      email = serializers.EmailField()

      def create(self, validated_data): #creer un Myuser avec les donnees recuperer
            user = models.MyUser.objects.create(
                  username = validated_data['login'],
                  email = validated_data['email']
            )
            return user



class   registerSerializer(serializers.Serializer): #class register
	username = serializers.CharField() #username 
	email = serializers.EmailField() #email ensure email format
	password1 = serializers.CharField(write_only=True) #password1 write only password never return in API responses
	password2 = serializers.CharField(write_only=True)




class loginSerializer(serializers.Serializer): #class login
    username = serializers.CharField() #username
    password = serializers.CharField() #password

class friendSerializer(serializers.Serializer): #class friend
	username = serializers.CharField() 


class nicknameSerializer(serializers.Serializer): #class nickname
	nickname = serializers.CharField()
      

class otpSerializer(serializers.Serializer):
    otp_code = serializers.CharField() #otp_code
    username = serializers.CharField() #username


class statsSerializer(serializers.Serializer):
	opponent = serializers.CharField()
	my_score = serializers.CharField()
	opponent_score = serializers.CharField()
	win = serializers.BooleanField()
      


class tournamentSerializer(serializers.Serializer):
	opponent = serializers.CharField()
	win = serializers.BooleanField()
      
class FriendsSerializer(serializers.ModelSerializer):
      class Meta:
            model = MyUser
            fields = ["id", "username"]