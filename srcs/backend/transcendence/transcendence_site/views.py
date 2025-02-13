from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from rest_framework import generics
from .models import MyUser
from .serializers import UserSerializer
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


# Create your views here.

def transcendence_site(request):
    return render(request, 'transcendence_site.html', {})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "User created !")
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'register.html', {'form': form})

def login_page(request):
    return render(request, 'login.html')


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
