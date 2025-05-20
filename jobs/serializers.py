from rest_framework import serializers
from .models import Company, JobOffer, Candidate, Application
from django.contrib.auth.models import User


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'website']

class JobOfferSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)

    class Meta:
        model = JobOffer
        fields = ['id', 'title', 'description', 'company', 'location', 'contract_type', 'published_at', 'deadline']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class CandidateSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Candidate
        fields = ['id', 'user', 'phone', 'bio', 'cv', 'skills']

class ApplicationSerializer(serializers.ModelSerializer):
    candidate = CandidateSerializer(read_only=True)
    job_offer = JobOfferSerializer(read_only=True)

    class Meta:
        model = Application
        fields = ['id', 'candidate', 'job_offer', 'cover_letter', 'applied_at', 'status']