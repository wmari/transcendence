from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class MyUser(AbstractUser):
    nickname = models.CharField(max_length=20)  #add nickname max 20character, plusieur personne peuvent avoir le meme nickname
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to='PPicture/', null=True, blank=True)
    friends = models.ManyToManyField("self", blank=True) #symmetrical=False check si on veut vrm cette option
    #check_online = models.BooleanField(default=False) #check si l'utilisateur est en ligne
    #check_ingame = models.BooleanField(default=False) #check si l'utilisateur est en jeu
    #check_oauth
    check_2fa = models.BooleanField(default=False) #check si l'utilisateur a activé l'authentification à 2 facteurs
    otp_code = models.CharField(max_length=6, blank=True, null=True) #code pour l'authentification à 2 facteurs, peut etre vide



    def __str__(self):
        return self.username 
    

#class UserStats(models.Model):

#class GameStats(models.Model):