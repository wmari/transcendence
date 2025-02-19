from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class MyUser(AbstractUser):
    nickname = models.CharField(max_length=20)  #add nickname max 20character, plusieur personne peuvent avoir le meme nickname
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to='PPicture/', default='PPicture/default.jpg') #add profile picture
    friends = models.ManyToManyField("self", blank=True) #symmetrical=False check si on veut vrm cette option
    check_online = models.BooleanField(default=False) #check si l'utilisateur est en ligne
    check_ingame = models.BooleanField(default=False) #check si l'utilisateur est en jeu
    check_oauth = models.BooleanField(default=False) #check si l'utilisatuer a active l'oauth
    check_2fa = models.BooleanField(default=False) #check si l'utilisateur a activé l'authentification à 2 facteurs
    otp_code = models.CharField(max_length=6, blank=True, null=True) #code pour l'authentification à 2 facteurs, peut etre vide



    def __str__(self):
        return self.username 
    

class UserStats(models.Model): #class stat game user
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, related_name='stat') #delete avec user , Allows reverse access from MyUser to UserStats using myuser_instance.stat
    number_of_game = models.PositiveIntegerField(default=0)
    number_of_win = models.PositiveIntegerField(default=0)
    number_of_defeat = models.PositiveIntegerField(default=0)
    win_percentage = models.PositiveSmallIntegerField(default=0)



class GameStats(models.Model): #class partie historique
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='games')
    win = models.BooleanField(blank=True, null=True)
    opponent = models.CharField(blank=True, null=True)
    my_score = models.PositiveSmallIntegerField(blank=True, null=True)
    opponent_score = models.PositiveSmallIntegerField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)