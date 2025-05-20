from django.db import models
from django.contrib.auth.models import User  # On utilisera User pour candidats/recruteurs

# Modèle Company (Entreprise)
class Company(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)

    def __str__(self):
        return self.name

# Modèle JobOffer (Offre d’emploi)
class JobOffer(models.Model):
    CONTRACT_TYPES = [
        ('FT', 'Temps plein'),
        ('PT', 'Temps partiel'),
        ('CT', 'Contrat temporaire'),
        ('IN', 'Stage / Internship'),
        ('FL', 'Freelance'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='job_offers')
    location = models.CharField(max_length=255)
    contract_type = models.CharField(max_length=2, choices=CONTRACT_TYPES)
    published_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.company.name}"

# Modèle Candidate (Candidat)
class Candidate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)
    cv = models.FileField(upload_to='cvs/', blank=True, null=True)
    skills = models.TextField(blank=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username

# Modèle Application (Candidature)
class Application(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='applications')
    job_offer = models.ForeignKey(JobOffer, on_delete=models.CASCADE, related_name='applications')
    cover_letter = models.TextField(blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('RE', 'Rejected'),
    ('AC', 'Accepted'),
    # autres statuts si besoin
]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    def __str__(self):
        return f"Candidature {self.candidate} pour {self.job_offer}"
