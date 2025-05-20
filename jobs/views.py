from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import  JobOffer, Candidate, Application, Company
from rest_framework import viewsets , permissions
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import RetrieveAPIView

from .serializers import JobOfferSerializer,CompanySerializer, JobOfferSerializer, CandidateSerializer, ApplicationSerializer

class JobOfferListView(ListView):
    model = JobOffer
    template_name = 'jobs/joboffer_list.html'
    context_object_name = 'job_offers'
    ordering = ['-published_at']
    paginate_by = 10  # pagination, 10 offres par page

class JobOfferDetailView(DetailView):
    model = JobOffer
    template_name = 'jobs/joboffer_detail.html'
    context_object_name = 'job_offer'

class JobOfferDetailAPIView(RetrieveAPIView):
    queryset = JobOffer.objects.all()
    serializer_class = JobOfferSerializer

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
class JobOfferViewSet(viewsets.ModelViewSet):
    queryset = JobOffer.objects.all().order_by('-published_at')
    serializer_class = JobOfferSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['location', 'contract_type', 'company']

class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

