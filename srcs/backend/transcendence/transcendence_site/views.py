from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from rest_framework import generics
from .models import MyUser, UserStats, GameStats
from .serializers import UserSerializer, nicknameSerializer, registerSerializer, loginSerializer, friendSerializer, otpSerializer, statsSerializer, tournamentSerializer
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.validators import validate_email #importer la fonction validate_email
from django.core.exceptions import ValidationError #importer la classe ValidationError
from django.contrib.auth import authenticate, login, logout #importer les fonctions authenticate et login
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie #importer les décorateurs csrf_exempt et ensure_csrf_cookie
from django.middleware.csrf import get_token #importer la fonction get_token
from django.http import HttpResponse, JsonResponse #importer les classes HttpResponse et JsonResponse
import random #importer le module random
from .utils import generate_otp_code, send_otp_email #importer les fonctions generate_otp et send_otp_email
import requests, os, re, random, string  #importer les modules
from rest_framework.views import APIView



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
                validate_email(email) #vérifier le format de l'email
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
            user.stat = UserStats.objects.create(user=user) #créer les statistiques de l'utilisateur
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

                if not user.check_2fa: #vérifier si l'utilisateur a activé l'authentification à deux facteurs

                    login(request, user) #builtin connecter l'utilisateur
                    user.check_online = True #mettre l'utilisateur en ligne
                    user.save() #sauvegarder les modifications
                    token = AccessToken.for_user(user) #générer un token
                    encoded_token = str(token) #encoder le token
                    refresh = RefreshToken.for_user(user)
                    user_data = { #créer un dictionnaire avec les données de l'utilisateur
                        'message': 'Connexion réussie.', #message de succès
					    'username' : getattr(user, 'username', 'unknown'), #récupérer le username de l'utilisateur
					    'nickname' : getattr(user, 'nickname', 'unknown'), #récupérer le nickname de l'utilisateur
					    'email' : getattr(user, 'email', 'unknown'), #récupérer l'email de l'utilisateur
					    'access': encoded_token, #récupérer le token
                        'refresh': str(refresh),
                    }
                    return Response(user_data, status=status.HTTP_200_OK) #retourner les données de l'utilisateur

                else:
                    otp = generate_otp_code() #générer un code otp
                    user.otp_code = otp #enregistrer le code otp
                    user.save() #sauvegarder les modifications
                    send_otp_email(user.email, otp) #envoyer le code otp par email
                    return Response({"message": "Veuillez entrer le code OTP pour vous connecter.", 'username': username}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Nom d'utilisateur ou mot de passe incorrect."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": serializer.errors}, status=401) #retourner les erreurs de validation
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        if request.method == 'POST': #vérifier si la méthode est POST
            if request.user.is_authenticated: #vérifier si l'utilisateur est authentifié
                request.user.check_online = False #mettre l'utilisateur hors ligne
                request.user.save() #sauvegarder les modifications
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



@ensure_csrf_cookie
def get_csrf_token(request): #obtenir le token csrf
    try:
        csrf_token = get_token(request) #builtin obtenir le token csrf
        return JsonResponse({"csrftoken": csrf_token}, status=status.HTTP_200_OK) #retourner le token csrf
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



def generate_otp():
    return ''.join(random.choices(string.digits, k=6)) #générer un code otp de 6 chiffres





@api_view(['POST'])
def check_otp_view(request):
    try:
        serializer = otpSerializer(data=request.data) #créer une instance de otpSerializer avec les données de la requête
        if serializer.is_valid(): #vérifier si les données sont valides
            otp_data = serializer.validated_data #récupérer les données validées dans otp_data
            user = MyUser.objects.get(username=otp_data['username']) #récupérer l'utilisateur
            if user.otp_code == otp_data['otp_code']: #vérifier si le code otp est correct
                login(request, user) #builtin connecter l'utilisateur
                user.check_online = True #mettre l'utilisateur en ligne
                user.save()
                token = AccessToken.for_user(user)
                encoded_token = str(token)
                user_data = {
                    'message': 'Connexion réussie.',
                    'username': getattr(user, 'username', 'unknown'),
                    'nickname': getattr(user, 'nickname', 'unknown'),
                    'email': getattr(user, 'email', 'unknown'),
                    'jwt_token': encoded_token,
                }
                return Response(user_data, status=status.HTTP_200_OK) #retourner les données de l'utilisateur
            else: #si le code otp est incorrect
                return Response({"error": "Code OTP incorrect."}, status=status.HTTP_400_BAD_REQUEST)
        else: #si les données ne sont pas valides
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e: #attraper les exceptions
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def uploadpp(request):
    if request.method == 'POST' and request.FILES.get['profile_picture']: #vérifier si la méthode est POST et si un fichier est envoyé
        user = request.user #récupérer l'utilisateur
        user.profile_picture = request.FILES.get['profile_picture'] #modifier la photo de profil de l'utilisateur
        user.save() #sauvegarder les modifications
        return JsonResponse({"message": "Photo de profil mise à jour avec succès."}, status=status.HTTP_200_OK)
    else: #si la méthode n'est pas POST ou si aucun fichier n'est envoyé
        return JsonResponse({"error": "Méthode non autorisée ou Pas d'image envoye"}, status=status.HTTP_400_BAD_REQUEST)




class profilView(APIView):
    def get(self, request): #fetch logged in user profil data
        try:
            user = request.user #recupere le user logged in 
            if user is not None: #si le user existe
                stat = user.stat #recupere les Userstat
                friend_list = [] #creer une liste friend vide
                if user.friends.all().count() > 0: #si il a au moins un ami
                    for friend in user.friends.all(): #ajoute les ami un par un
                        friend_list.append({
							'username': friend.username,
							'nickname': friend.nickname,
							'ingame': friend.check_ingame,
							'online': friend.check_online,
							'profile_picrture': friend.profile_picture.url,
                        })
                game_list = []  #liste game vide
                if user.games.all().count() > 0: #si au moins une game
                    for game in user.games.all():
                        if game.opponent == 'Tournament': #si les donnees dun tournoi
                            game_list.append({
								'opponent': game.opponent,
								'win': game.win,
								'date': game.date,
                            })
                        else: #sinon
                            game_list.append({
								'opponent': game.opponent,
								'win': game.win,
								'my_score': game.my_score,
								'opponent_score': game.opponent_score,
								'date': game.date,
                            })
                data = { #creer un dictionnaire avec les data du user logged in
					'nickname': user.nickname,
					'email': user.email,
					'profile_picture': user.profile_picture.url,
					'number_of_game': stat.number_of_game,
					'number_of_win': stat.number_of_win,
					'number_of_defeat': stat.number_of_defeat,
					'win_percentage': stat.win_percentage,
					'friends': friend_list,
					'games': game_list,
				}
                return JsonResponse({'data': data}, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def post(self, request): #fetch another user profile based on username
        try:
            try:
                user = MyUser.objects.get(username=request.data['username']) #recupere le user du username dans la requete
            except MyUser.DoesNotExist: #si le user nexiste pas
                return Response({"error": "Utilisateur non existant."}, status=status.HTTP_400_BAD_REQUEST)
            if user is not None: #si le user existe
                stat = user.stat #recupere les stat
                friend_list = [] #fiend liste vide
                if user.friends.all().count() > 0: #si au moins un ami
                    for friend in user.friends.all(): #ajoute les amis un par un
                        friend_list.append({ 
							'username': friend.username,
							'nickname': friend.nickname,
							'ingame': friend.check_ingame,
							'online': friend.check_online,
							'profil_image': friend.profil_image.url,
                        })
                game_list = []
                if user.games.all().count() > 0:
                    for game in user.games.all():
                        if game.opponent == 'Tournament':
                            game_list.append({
								'opponent': game.opponent,
								'win': game.win,
								'date': game.date,
                            })
                        else:
                            game_list.append({
								'opponent': game.opponent,
								'win': game.win,
								'my_score': game.my_score,
								'opponent_score': game.opponent_score,
								'date': game.date,                               
                            })
                data = { #build un dictionnaire avec les donnees du user de la requete
					'message': 'Other profile',
					'nickname': user.nickname,
					'email': user.email,
					'profile_picture': user.profile_picture.url,
					'number_of_game': stat.number_of_game,
					'number_of_win': stat.number_of_win,
					'number_of_defeat': stat.number_of_defeat,
					'win_percentage': stat.win_percentage,
					'friends': friend_list,
					'games': game_list,
                }
                return JsonResponse({'data': data}, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)            




@api_view(['POST'])
def game_end_view(request): #fin de game, recupere les donnees de la partie et les sauvegarde, update les stats du user
	try:
		serializer = statsSerializer(data=request.data) #creer une instance stat serializer et recupere les donnees de la requete
		if serializer.is_valid(): #si le donnees sont valides
			game_data = serializer.validated_data #game_data recupere les datas
			user = request.user #recupere le user demandant la requete
			stat = user.stat #recupere les stats du user
			stat.number_of_game += 1
			if game_data['win'] == True:
				stat.number_of_win += 1
			else:
				stat.number_of_defeat += 1
			stat.win_percentage = stat.number_of_win / user.stat.number_of_game * 100 #calcul le taux de victoire
			stat.save()
			user.save()
			new_game = GameStats.objects.create(user=user, win=game_data['win'], opponent=game_data['opponent'], my_score=game_data['my_score'], opponent_score=game_data['opponent_score']) #creer une nouvelle instance gamestats et recupere les donnes de la partie
			new_game.save()
			return Response({'message': 'Data send successfully'}, status=status.HTTP_200_OK)    
		else:
			return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
	except Exception as e:
		return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#The API accepts game data in a POST request.
#The data is validated using a serializer.
#The user’s game stats are updated (number of games, wins, defeats, win percentage).
#A new game record is created and saved.
#A success message is returned, or if an error occurs, an error message is returned.



@api_view(['POST'])
def tournament_view(request):
	try:
		serializer = tournamentSerializer(data=request.data)
		if serializer.is_valid():
			game_data = serializer.validated_data
			user = request.user
			user.stat.number_of_game += 1
			if game_data['win'] == True:
				user.stat.number_of_win += 1
			else:
				user.stat.number_of_defeat += 1
			user.stat.win_percentage = user.stat.number_of_win / user.stat.number_of_game * 100
			user.game = GameStats.objects.create(user=user, win=game_data['win'], opponent=game_data['opponent'])
			user.save()
			return Response({'message': 'Data send successfully'}, status=status.HTTP_200_OK)    
		else:
			return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
	except Exception as e:
		return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#The API receives the result of a tournament game via a POST request.
#The data is validated using tournamentSerializer.
#The user's stats (number of games, wins, defeats, win percentage) are updated based on the result.
#A new game record is created for the user, with the tournament as the opponent.
#The updated user data is saved to the database.
#A success message is returned to the client, or an error message is sent if something goes wrong.



@api_view(['GET'])
def ingame_view(request):
	try:
		user = request.user
		user.check_ingame = True
		user.save()
		return Response(status=status.HTTP_200_OK)
	except Exception as e:
		return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#The view is triggered by a GET request to the ingame_view endpoint.
#The authenticated user is retrieved from the request.
#The user's ingame status is set to True.
#The user object is saved to reflect the change.
#If successful, a 200 OK response is returned. If any error occurs, a 400 Bad Request response with an error message is returned.





@api_view(['GET'])
def not_ingame_view(request):
	try:
		if request.user.is_authenticated:
			user = request.user
			user.check_ingame = False
			user.save()
		return Response(status=status.HTTP_200_OK)
	except Exception as e:
		return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#The view is triggered by a GET request to the not_ingame_view endpoint.
#The code checks if the user is authenticated.
#If authenticated, the user's ingame status is set to False, indicating they are not currently in a game.
#The updated user object is saved to the database.
#A 200 OK response is returned if everything is successful. If an error occurs, a 400 Bad Request response with an error message is returned.






#oauth42login

#oauth42get_user