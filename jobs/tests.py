from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from .models import Company, JobOffer, Candidate, Application
from django.test import TestCase
from django.contrib.auth import get_user_model


class JobOfferAPITest(APITestCase):
    def setUp(self):
        # Création d’un user et d’une company
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.company = Company.objects.create(name='Test Company', description='Desc', website='https://test.com')

        # Création d’une offre d’emploi
        self.job_offer = JobOffer.objects.create(
            title='Developer',
            description='Job description',
            location='Remote',
            company=self.company,
            contract_type='Full-time',
        )
    
    def test_list_job_offers(self):
        url = reverse('jobs:joboffer_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Developer', str(response.content))

    def test_retrieve_job_offer(self):
        url = reverse('joboffer-detail', kwargs={'pk': self.job_offer.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'Developer')



class CompanyModelTest(TestCase):
    def test_create_company(self):
        company = Company.objects.create(
            name='EcoCorp',
            description='Entreprise éco-responsable',
            website='https://ecocorp.com'
        )
        self.assertEqual(company.name, 'EcoCorp')
        self.assertEqual(company.website, 'https://ecocorp.com')
       

User = get_user_model()

class CandidateModelTest(TestCase):
    def test_create_candidate(self):
        user = User.objects.create_user(username='candidateuser', password='testpass')
        candidate = Candidate.objects.create(user=user)
        self.assertEqual(candidate.user.username, 'candidateuser')



class ApplicationModelTest(TestCase):
    def test_create_application(self):
        user = User.objects.create_user(username='candidat2', password='pass123')
        candidate = Candidate.objects.create(user=user)
        company = Company.objects.create(name='EcoInc', description='...', website='https://eco.com')
        job = JobOffer.objects.create(
            title='Ingénieur',
            description='Offre test',
            company=company,
            location='Douala',
            contract_type='CDI'
        )
        application = Application.objects.create(
            job_offer=job,
            candidate=candidate,
            cover_letter='Motivé et disponible'
        )
        self.assertEqual(application.status, 'pending')


class JWTAuthTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')

    def test_jwt_auth(self):
        url = '/api/token/'
        response = self.client.post(url, {'username': 'testuser', 'password': 'testpass123'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)


class JobOfferAPITest(TestCase):
    def setUp(self):
        self.job_offer = JobOffer.objects.create(
            title='Developer',
            description='Python Developer',
            location='Remote',
            company='TechCorp',
        )

    def test_retrieve_job_offer(self):
        url = reverse('joboffer-detail', kwargs={'pk': self.job_offer.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'Developer')  # maintenant, response.data est bien dispo