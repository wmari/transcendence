from django.urls import path
from transcendence_site import views
from django.conf import settings
from django.conf.urls.static import static
from .views import UserListCreateView, UserDetailView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import get_user, add_friend, remove_friend
from . import views


urlpatterns = [
    path('', views.transcendence_site, name='transcendence_site'),
    path('api/users/', UserListCreateView.as_view(), name='user-list-create'),
    path('api/users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/user/', get_user, name='get_user'),
    path('api/friends/add/<int:friend_id>/', add_friend, name='add_firend'),
    path('api/friends/remove/<int:friend_id>/', remove_friend, name='remove_friend'),
    path('api/nickname/', views.modif_nickname, name='nickname'),  #path pour modifier le nickname
    path('api/register/', views.register_view, name='register'),  #path pour s'enregistrer
    path('api/login/', views.login_view, name='login'),  #path pour se connecter
    path('api/logout/', views.logout_view, name='logout'),  #path pour se deconnecter
    path('api/addfriend/', views.add_friend, name='addfriend'),  #path pour ajouter un ami
    path('api/get-csrf-token/', views.get_csrf_token, name='csrf_token'), #path pour obtenir le token csrf
	path('api/check_2fa/', views.check_otp_view, name='check_2fa'), #path pour verifier le code otp 2fa
    path('api/uploadpp/', views.uploadpp, name='uploadpp'), #path pour upload une photo de profil
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)