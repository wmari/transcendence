from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import MyUser

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    profil_picture = forms.ImageField(required=False)

    class Meta:
        model = MyUser
        fields = ['username', 'email', 'profil_picture', 'password1', 'password2']