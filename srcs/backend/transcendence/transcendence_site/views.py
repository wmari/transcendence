from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from rest_framework import generics
from .models import MyUser
from .serializers import UserSerializer, nicknameSerializer
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


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
