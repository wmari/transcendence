from django.urls import path
from hello_world import views
from django.conf import settings
from django.conf.urls.static import static
from .views import register
from .views import login_page

urlpatterns = [
    path('', views.hello_world, name='hello_world'),
    path('register/', register, name='register'),
    path('login/', login_page, name='login'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)