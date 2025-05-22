from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class User(AbstractUser):
    ROLE_CHOICES = [
        ('collector', 'Collecteur'),
        ('recruiter', 'Recruteur'),
        ('buyer', 'Acheteur'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='collector')
    phone = models.CharField(max_length=20, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    class Meta:
        swappable = 'AUTH_USER_MODEL'
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'



class Company(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Nom de l'entreprise"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    website = models.URLField(blank=True, verbose_name=_("Site web"))
    logo = models.ImageField(
        upload_to='company_logos/',
        blank=True,
        null=True,
        verbose_name=_("Logo")
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Entreprise")
        verbose_name_plural = _("Entreprises")
        ordering = ['name']

    def __str__(self):
        return self.name

class JobOffer(models.Model):
    class ContractType(models.TextChoices):
        FULL_TIME = 'FT', _('Temps plein')
        PART_TIME = 'PT', _('Temps partiel')
        TEMPORARY = 'CT', _('Contrat temporaire')
        INTERNSHIP = 'IN', _('Stage')
        FREELANCE = 'FL', _('Freelance')
    
    title = models.CharField(max_length=255, verbose_name=_("Titre du poste"))
    description = models.TextField(verbose_name=_("Description"))
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='job_offers',
        verbose_name=_("Entreprise")
    )
    location = models.CharField(max_length=255, verbose_name=_("Localisation"))
    contract_type = models.CharField(
        max_length=2,
        choices=ContractType.choices,
        verbose_name=_("Type de contrat")
    )
    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_("Salaire")
    )
    requirements = models.TextField(blank=True, verbose_name=_("Exigences"))
    is_active = models.BooleanField(default=True, verbose_name=_("Active"))
    published_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Date de publication"))
    deadline = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name=_("Date limite")
    )

    class Meta:
        verbose_name = _("Offre d'emploi")
        verbose_name_plural = _("Offres d'emploi")
        ordering = ['-published_at']
        indexes = [
            models.Index(fields=['-published_at']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.title} - {self.company.name}"

class Application(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', _('En attente')
        REVIEWED = 'reviewed', _('Examinée')
        INTERVIEW = 'interview', _('Entretien')
        ACCEPTED = 'accepted', _('Acceptée')
        REJECTED = 'rejected', _('Rejetée')
    
    candidate = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='applications',
        verbose_name=_("Candidat")
    )
    job_offer = models.ForeignKey(
        JobOffer,
        on_delete=models.CASCADE,
        related_name='applications',
        verbose_name=_("Offre d'emploi")
    )
    cover_letter = models.TextField(blank=True, verbose_name=_("Lettre de motivation"))
    cv = models.FileField(
        upload_to='cvs/%Y/%m/%d/',
        validators=[FileExtensionValidator(['pdf', 'doc', 'docx'])],
        verbose_name=_("CV")
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name=_("Statut")
    )
    applied_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Date de candidature"))
    notes = models.TextField(blank=True, verbose_name=_("Notes"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Dernière mise à jour"))

    class Meta:
        verbose_name = _("Candidature")
        verbose_name_plural = _("Candidatures")
        ordering = ['-applied_at']
        unique_together = ['candidate', 'job_offer']
        indexes = [
            models.Index(fields=['-applied_at']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.candidate} - {self.job_offer}"

class Candidate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='candidate_profile')
    bio = models.TextField(blank=True, null=True)
    education = models.TextField(blank=True, null=True)
    experience = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username


# models.py
class WasteCollection(models.Model):
    collecteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    waste_type = models.CharField(max_length=100)
    quantity_grams = models.FloatField()  # poids brut en grammes
    hours_worked = models.FloatField()
    date_collected = models.DateField(auto_now_add=True)

    def quantity_kg(self):
        return self.quantity_grams / 1000

    def estimated_revenue(self):
        return self.quantity_kg() * 50  # exemple: 50 FCFA/kg
