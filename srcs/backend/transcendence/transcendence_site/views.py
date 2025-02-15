from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from rest_framework import generics
from .models import MyUser
from .serializers import UserSerializer, nicknameSerializer, registerSerializer
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.validators import validate_email #importer la fonction validate_email
from django.core.exceptions import ValidationError #importer la classe ValidationError

# Create your views here.

def transcendence_site(request):
    return render(request, 'transcendence_site.html', {})

class UserListCreateView(generics.ListCreateAPIView):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer

# Vues d'authentification pour le token JWT
class CustomTokenObtainPairView(TokenObtainPairView):
    # Personnaliser l'obtention du token si nécessaire
    pass

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request):
    user = request.user
    return Response({"username": user.username, "email": user.email})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_friend(request, friend_id):
    user = request.user
    try:
        friend = MyUser.objects.get(id=friend_id)
        if friend == user:
            return Response({"error" : "Vous ne pouvez pas vous ajouter vous-même"}, status=status.HTTP_400_BAD_REQUEST)
        
        user.friends.add(friend)
        return Response({"message": "Ami ajouté avec succès."}, status=status.HTTP_200_OK)
    
    except MyUser.DoesNotExist:
        return Response({"error": "Utilisateur introuvable."}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_friend(request, friend_id):
    user = request.user
    try:
        friend = MyUser.objects.get(id=friend_id)
        user.friends.remove(friend)
        return Response({"message": "Ami supprimé avec succès."}, status=status.HTTP_200_OK)

    except MyUser.DoesNotExist:
        return Response({"error": "Utilisateur introuvable."}, status=status.HTTP_404_NOT_FOUND)




#endpoint a gérer_________________________________________________________________________________________

@api_view(['POST'])
def modif_nickname(request):    #modifier le nickname
    try:
        serializer = nicknameSerializer(data=request.data)  #créer une instance de nicknameSerializer avec les données de la requête
        if serializer.is_valid(): #vérifier si les données sont valides
            data = serializer.validated_data #récupérer les données validées dans data
            nickname = data['nickname'] #récupérer le nickname
            request.user.nickname = nickname #modifier le nickname de l'utilisateur
            request.user.save() #sauvegarder les modifications
            return Response({"message": "Nickname modifié avec succès."}, status=status.HTTP_200_OK) #retourner un message de succès
        else:
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST) #retourner les erreurs de validation
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) #retourner l'erreur catch





@api_view(['POST']) 
def register_view(request): 
    try:
        serializer = registerSerializer(data=request.data)  #créer une instance de registerSerializer avec les données de la requête
        if serializer.is_valid(): #vérifier si les données sont valides
            data = serializer.validated_data #récupérer les données validées dans data
            username = data['username'] #récupérer le username
            email = data['email'] #récupérer l'email
            password1 = data['password1'] #récupérer le password1
            password2 = data['password2'] #récupérer le password2


            try:
                validate_emal(email) #vérifier le format de l'email
            except ValidationError :
                return Response({"error": "Format d'email invalide."}, status=status.HTTP_400_BAD_REQUEST)
            
            if password1 != password2: #vérifier si les mots de passe correspondent
                return Response({"error": "Les mots de passe ne correspondent pas."}, status=status.HTTP_400_BAD_REQUEST)
            
            if len(password1) < 8: #vérifier si le mot de passe contient au moins 8 caractères
                return Response({"error": "Le mot de passe doit contenir au moins 8 caractères."}, status=status.HTTP_400_BAD_REQUEST)

            if not re.findall('[A-Z]', password1): #vérifier si le mot de passe contient au moins une lettre majuscule
                return Response({"error": "Le mot de passe doit contenir au moins une lettre majuscule."}, status=status.HTTP_400_BAD_REQUEST)

            if not re.findall('[a-z]', password1): #vérifier si le mot de passe contient au moins une lettre minuscule
                return Response({"error": "Le mot de passe doit contenir au moins une lettre minuscule."}, status=status.HTTP_400_BAD_REQUEST)

            if not re.findall('[0-9]', password1): #vérifier si le mot de passe contient au moins un chiffre
                return Response({"error": "Le mot de passe doit contenir au moins un chiffre."}, status=status.HTTP_400_BAD_REQUEST)
            
            if not re.findall(r'\W', password1): #vérifier si le mot de passe contient au moins un caractère spécial
                return Response({"error": "Le mot de passe doit contenir au moins un caractère spécial."}, status=status.HTTP_400_BAD_REQUEST)

            if (MyUser.objects.filter(username=username).exists()): #vérifier si le username existe déjà
                return Response({"error": "Ce nom d'utilisateur existe déjà."}, status=status.HTTP_400_BAD_REQUEST)

            if (MyUser.objects.filter(email=email).exists()): #vérifier si l'email existe déjà 
                return Response({"error": "Cet email existe déjà."}, status=status.HTTP_400_BAD_REQUEST)

            user = MyUser.objects.create_user(username=username, email=email, password=password1, nickname=username) #créer un utilisateur
            #user.stat = Stats.objects.create(user=user) #créer les statistiques de l'utilisateur
            return Response({"message": "Utilisateur créé avec succès."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST) #retourner les erreurs de validation
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


