from django.contrib import admin
from .models import Company, JobOffer, Candidate, Application

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'website')
    search_fields = ('name',)

@admin.register(JobOffer)
class JobOfferAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location', 'contract_type', 'published_at')
    list_filter = ('contract_type', 'published_at')
    search_fields = ('title', 'company__name', 'location')

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'job_offer', 'status', 'applied_at')
    list_filter = ('status', 'applied_at')
    search_fields = ('candidate__user__username', 'job_offer__title')
