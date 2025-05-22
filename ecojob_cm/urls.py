from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView  # Ajouté
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from jobs.views import  RecruteurDashboardView, AcheteurDashboardView, LoginView
from drf_yasg import openapi
from jobs import views
from jobs.views import CollecteurDashboardView,UserRegisterView, UserLoginView, UserView, EmailTokenObtainPairView, collecteur_dashboard
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Import UserRegisterView and other user-related views
# Ensure the 'user' app is in INSTALLED_APPS and 'user/views.py' exists
try:
    from jobs.views import UserRegisterView, UserLoginView, UserView
except ModuleNotFoundError as e:
    raise ImportError("Could not import from 'user.views'. Make sure the 'user' app exists and contains 'views.py' with the required views.") from e

schema_view = get_schema_view(
   openapi.Info(
      title="EcoJob API",
      default_version='v1',
      description="Documentation de l'API EcoJob",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Route pour la racine - Redirection vers Swagger ou page d'accueil
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    
    # Administration Django
    path("admin/", admin.site.urls),
    
    # URLs de l'application jobs
    path('jobs/', include('jobs.urls', namespace='jobs')),
    
    # Authentification JWT
   
    # path('api/token/', EmailTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', UserRegisterView.as_view(), name='register'),
    path('api/token', EmailTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('collecteur/dashboard.html/', CollecteurDashboardView.as_view(), name='collecteur-dashboard'),
    path('collecteur/dashboard.html/', views.collecteur_dashboard, name='collecteur-dashboard'),
    path('recruteur/dashboard.html', RecruteurDashboardView.as_view(), name='recruteur-dashboard'),
    path('acheteur/dashboard.html', AcheteurDashboardView.as_view(), name='acheteur-dashboard'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/user/me/', UserView.as_view(), name='user-profile'),
    
    # Documentation API
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]