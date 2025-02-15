from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class MyUser(AbstractUser):
    nickname = models.CharField(max_length=20)  #add nickname max 20character, plusieur personne peuvent avoir le meme nickname
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to='PPicture/', null=True, blank=True)
    friends = models.ManyToManyField("self", symmetrical=False, blank=True) #symmetrical=False check si on veut vrm cette option

    def __str__(self):
        return self.username
    
