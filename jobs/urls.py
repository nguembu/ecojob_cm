from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CompanyViewSet,
    JobOfferViewSet,
    CandidateViewSet,
    ApplicationViewSet,
    JobOfferListView,
    JobOfferDetailView,
    JobOfferDetailAPIView,
    UserRegisterView,
    UserView,
    UserLoginView
    
)
from rest_framework_simplejwt.views import TokenObtainPairView

app_name = 'jobs'

router = DefaultRouter()
router.register(r'api/companies', CompanyViewSet, basename='company')
router.register(r'api/joboffers', JobOfferViewSet, basename='joboffer')
router.register(r'api/candidates', CandidateViewSet, basename='candidate')
router.register(r'api/applications', ApplicationViewSet, basename='application')

urlpatterns = [
    path('', JobOfferListView.as_view(), name='joboffer_list'),
    path('<int:pk>/', JobOfferDetailView.as_view(), name='joboffer_detail'),
    path('api/joboffers/<int:pk>/', JobOfferDetailAPIView.as_view(), name='joboffer-detail'),
    path('', include(router.urls)),  # Ajoute les routes API sous /jobs/api/joboffers/
]
