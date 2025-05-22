from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import JobOffer, Application, Company, User , Candidate, WasteCollection

from rest_framework import viewsets, permissions, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.decorators import login_required
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from django.views.generic import TemplateView
from rest_framework.exceptions import AuthenticationFailed
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.decorators import api_view, permission_classes
from .serializers import (
    JobOfferSerializer,
    CompanySerializer,
    CandidateSerializer,
    ApplicationSerializer,
    UserRegisterSerializer,
    UserLoginSerializer,
    UserSerializer,
    EmailTokenObtainPairSerializer
)

# Views pour le frontend Django
class JobOfferListView(ListView):
    model = JobOffer
    template_name = '../templates/jobs/joboffer_list.html'
    context_object_name = 'job_offers'
    ordering = ['-published_at']
    paginate_by = 10

class JobOfferDetailView(DetailView):
    model = JobOffer
    template_name = '../templates/jobs/joboffer_detail.html'
    context_object_name = 'job_offers'

# API Views
class JobOfferDetailAPIView(RetrieveAPIView):
    queryset = JobOffer.objects.all()
    serializer_class = JobOfferSerializer
    permission_classes = [AllowAny]

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]

class JobOfferViewSet(viewsets.ModelViewSet):
    queryset = JobOffer.objects.all().order_by('-published_at')
    serializer_class = JobOfferSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['location', 'contract_type', 'company']

class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    permission_classes = [IsAuthenticated]

class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

# Authentification et gestion utilisateur
@method_decorator(csrf_exempt, name='dispatch')
class UserRegisterView(CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        data = {
            'user': UserRegisterSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return Response(data, status=status.HTTP_201_CREATED)


class UserLoginView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer
# class UserLoginView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         email = request.data.get('email')
#         password = request.data.get('password')

#         user = authenticate(request, email=email, password=password)

#         if user:
#             refresh = RefreshToken.for_user(user)
#             return Response({
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token),
#                 'role': user.role,
#             })
#         else:
#             return Response({'error': 'Email ou mot de passe invalide'}, status=status.HTTP_401_UNAUTHORIZED)
class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'username': user.username,
            'email': user.email,
            'role': user.role
        })
class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = User.EMAIL_FIELD

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(request=self.context.get("request"), email=email, password=password)

        if not user:
            raise AuthenticationFailed('Email ou mot de passe incorrect')

        data = super().validate(attrs)
        data["user"] = {
            "username": user.username,
            "email": user.email,
            "role": user.role,
        }

        return data

class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer
    
    

class RecruteurDashboardView(TemplateView):
    template_name = 'recruteur/dashboard.html'

class AcheteurDashboardView(TemplateView):
    template_name = 'acheteur/dashboard.html'



class CollecteurDashboardView(TemplateView):
     template_name = 'collecteur/dashboard.html'
   
class LoginView(TemplateView):
    template_name = "login.html"
    
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def collecteur_dashboard(request):
#     user = request.user
#     initial = (user.first_name or user.username or "U")[0].upper()
#     return Response({
#         'username': user.first_name or user.username,
#         'initial': initial
#     })


@login_required
def collecteur_dashboard(request):
    user = request.user
    collections = WasteCollection.objects.filter(collecteur=user)

    total_kg = sum([c.quantity_grams for c in collections]) / 1000
    total_hours = sum([c.hours_worked for c in collections])
    total_revenue = total_kg * 50  # exemple de tarif

    return render(request, 'dashboard.html', {
        'total_kg': total_kg,
        'total_hours': total_hours,
        'total_revenue': total_revenue,
        'collections': collections
    })
