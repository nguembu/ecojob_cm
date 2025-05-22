from rest_framework import serializers
from .models import Company, JobOffer, Candidate, Application, User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'website', 'description', 'logo']
        read_only_fields = ['id']

class JobOfferSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    company_id = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(),
        source='company',
        write_only=True,
        required=False
    )

    class Meta:
        model = JobOffer
        fields = [
            'id', 'title', 'description', 'company', 'company_id',
            'location', 'contract_type', 'salary', 'published_at',
            'deadline', 'requirements', 'is_active'
        ]
        read_only_fields = ['id', 'published_at']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['role', 'phone', 'address', 'profile_picture']
        read_only_fields = ['role']

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'date_joined', 'profile'
        ]
        read_only_fields = ['id', 'date_joined']

class CandidateSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='user',
        write_only=True
    )

    class Meta:
        model = Candidate
        fields = [
            'id', 'user', 'user_id', 'phone', 'bio',
            'cv', 'skills', 'experience_years', 'education'
        ]
        read_only_fields = ['id']

class ApplicationSerializer(serializers.ModelSerializer):
    candidate = CandidateSerializer(read_only=True)
    job_offer = JobOfferSerializer(read_only=True)
    candidate_id = serializers.PrimaryKeyRelatedField(
        queryset=Candidate.objects.all(),
        source='candidate',
        write_only=True
    )
    job_offer_id = serializers.PrimaryKeyRelatedField(
        queryset=JobOffer.objects.all(),
        source='job_offer',
        write_only=True
    )

    class Meta:
        model = Application
        fields = [
            'id', 'candidate', 'candidate_id', 'job_offer', 'job_offer_id',
            'cover_letter', 'applied_at', 'status', 'notes'
        ]
        read_only_fields = ['id', 'applied_at']

# Authentification Serializers

User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES, required=True)

    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name', 'role']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Les mots de passe ne correspondent pas."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        role = validated_data.pop('role')

        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            role=role
        )
        user.set_password(validated_data['password'])
        user.save()
        return user



class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    

class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = User.EMAIL_FIELD  # "email"

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            # Passe email en username
            user = authenticate(request=self.context.get('request'), email=email, password=password)

            if not user:
                raise serializers.ValidationError("Email ou mot de passe incorrect.")

            data = super().validate({
                self.username_field: email,
                'password': password
            })

            data['user'] = {
                'username': user.username,
                'email': user.email,
                'role': user.role
            }

            return data
        else:
            raise serializers.ValidationError("Email et mot de passe requis.")