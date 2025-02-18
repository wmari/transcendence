from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import MyUser
from django.contrib.auth import login, authenticate

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



#class Oauthuserserializer , define login et password 
#create user en utilisant ces donnees et return le user

#class login
#class firend
#class game_stats
#class tournament_stats
#class otp







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