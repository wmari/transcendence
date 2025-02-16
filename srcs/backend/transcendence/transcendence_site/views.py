from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from rest_framework import generics
from .models import MyUser
from .serializers import UserSerializer, nicknameSerializer, registerSerializer, loginSerializer
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.validators import validate_email #importer la fonction validate_email
from django.core.exceptions import ValidationError #importer la classe ValidationError
from django.contrib.auth import authenticate, login, logout #importer les fonctions authenticate et login
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie #importer les décorateurs csrf_exempt et ensure_csrf_cookie
from django.middleware.csrf import get_token #importer la fonction get_token
from django.http import HttpResponse, JsonResponse #importer les classes HttpResponse et JsonResponse

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

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def add_friend(request, friend_id):
#     user = request.user
#     try:
#         friend = MyUser.objects.get(id=friend_id)
#         if friend == user:
#             return Response({"error" : "Vous ne pouvez pas vous ajouter vous-même"}, status=status.HTTP_400_BAD_REQUEST)
        
#         user.friends.add(friend)
#         return Response({"message": "Ami ajouté avec succès."}, status=status.HTTP_200_OK)
    
#     except MyUser.DoesNotExist:
#         return Response({"error": "Utilisateur introuvable."}, status=status.HTTP_404_NOT_FOUND)
    

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def remove_friend(request, friend_id):
#     user = request.user
#     try:
#         friend = MyUser.objects.get(id=friend_id)
#         user.friends.remove(friend)
#         return Response({"message": "Ami supprimé avec succès."}, status=status.HTTP_200_OK)

#     except MyUser.DoesNotExist:
#         return Response({"error": "Utilisateur introuvable."}, status=status.HTTP_404_NOT_FOUND)




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




@api_view(['POST'])
def login_view(request):
    try:
        serializer = loginSerializer(data=request.data) #créer une instance de loginSerializer avec les données de la requête
        if serializer.is_valid(): #vérifier si les données sont valides
            data = serializer.validated_data #récupérer les données validées dans data
            username = data['username'] #récupérer le username
            password = data['password'] #récupérer le password
            user = authenticate(username=username, password=password) #builtin authentifier l'utilisateur
            if user is not None: #vérifier si l'utilisateur existe

                #if not user.check_2fa: #vérifier si l'utilisateur a activé l'authentification à deux facteurs

                    login(request, user) #builtin connecter l'utilisateur
                    #user.check_online = True #mettre l'utilisateur en ligne
                    user.save() #sauvegarder les modifications
                    #token = AccessToken.for_user(user) #générer un token
                    #encoded_token = str(token) #encoder le token
                    user_data = { #créer un dictionnaire avec les données de l'utilisateur
                        'message': 'Connexion réussie.', #message de succès
					    'username' : getattr(user, 'username', 'unknown'), #récupérer le username de l'utilisateur
					    'nickname' : getattr(user, 'nickname', 'unknown'), #récupérer le nickname de l'utilisateur
					    'email' : getattr(user, 'email', 'unknown'), #récupérer l'email de l'utilisateur
					    #'jwt_token': encoded_token, #récupérer le token
                    }
                    return Response(user_data, status=status.HTTP_200_OK) #retourner les données de l'utilisateur
                #else:
                    #generate and save otp code
                    #send otp code to user
                    #return Response({"message": "Veuillez entrer le code OTP pour vous connecter."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Nom d'utilisateur ou mot de passe incorrect."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": serializer.errors}, status=status.HTTP_401_BAD_REQUEST) #retourner les erreurs de validation
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def logout_view(request):
    try:
        if request.method == 'POST': #vérifier si la méthode est POST
            if request.user.is_authenticated: #vérifier si l'utilisateur est authentifié
                #request.user.check_online = False #mettre l'utilisateur hors ligne
                #request.user.save() #sauvegarder les modifications
                logout(request) #builtin déconnecter l'utilisateur

            return JsonResponse({"message": "Déconnexion réussie."}, status=status.HTTP_200_OK) #retourner un message de succès
        else:
            return JsonResponse({"error": "Méthode non autorisée."}, status=status.HTTP_405_METHOD_NOT_ALLOWED) #retourner une erreur         
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def add_friend(request):
    try:
        serializer = friendSerializer(data=request.data) #créer une instance de friendSerializer avec les données de la requête
        if serializer.is_valid(): #vérifier si les données sont valides

            friend_data = serializer.validated_data #récupérer les données validées dans friend_data
            username = friend_data['username'] #récupérer le username
            if username == request.user.username: #vérifier si l'utilisateur essaie de s'ajouter lui-même
                return Response({"error": "Vous ne pouvez pas vous ajouter vous-même."}, status=status.HTTP_400_BAD_REQUEST)
            try:
                user_to_add = MyUser.objects.get(username=username) #récupérer l'utilisateur à ajouter
                if user_to_add in request.user.friends.all():
                    return Response({"error": "Cet utilisateur est déjà votre ami."}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    request.user.friends.add(user_to_add) #ajouter l'utilisateur en ami
                    return Response({"message": "Ami ajouté avec succès."}, status=status.HTTP_200_OK)
            except MyUser.DoesNotExist: #si l'utilisateur n'existe pas
                return Response({"error": "Utilisateur introuvable."}, status=status.HTTP_404_NOT_FOUND)
        else: #si les données ne sont pas valides
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e: #attraper les exceptions
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def accept_friend_request(request):
	return Response("accept friend request")


#oauth42login

#oauth42get_user

@ensure_csrf_cookie
def get_csrf_token(request): #obtenir le token csrf
    try:
        csrf_token = get_token(request) #builtin obtenir le token csrf
        return JsonResponse({"csrftoken": csrf_token}, status=status.HTTP_200_OK) #retourner le token csrf
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






#profilview

#generateotp
#verifyotp

#upload_avatar

#tournament

#checkingame

#checknotingame


