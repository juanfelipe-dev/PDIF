from django.test import TestCase, Client
from core.models import Organization
from .models import Submission, Question


class SubmissionTests(TestCase):
    def setUp(self):
        self.org = Organization.objects.create(name='Test Org', slug='test')
        Question.objects.create(organization=self.org, text='Q1', sort_order=1)

    def test_submission_and_pdf_generation(self):
        data = {'q_1': 'answer'}
        sub = Submission.objects.create(organization=self.org, data=data)
        # after creation, pdf field should be populated and sha calculated
        self.assertTrue(sub.pdf.name)
        self.assertEqual(len(sub.pdf_sha256), 64)


class ViewTests(TestCase):
    def setUp(self):
        self.org = Organization.objects.create(name='Test Org', slug='test')
        Question.objects.create(organization=self.org, text='Q1', sort_order=1)
        self.client = Client()

    def test_landing_page(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Begin Review')

    def test_questionnaire_post_and_download(self):
        # get initial page
        resp = self.client.get('/questionnaire/')
        self.assertEqual(resp.status_code, 200)
        # submit an answer
        resp = self.client.post('/questionnaire/', {'q_1': 'foo'})
        self.assertEqual(resp.status_code, 302)
        submission = Submission.objects.last()
        # follow redirect to completion
        resp = self.client.get(resp.url)
        self.assertContains(resp, 'Download PDF')
        token = resp.context['download_token']
        # access download
        dl = self.client.get(f'/download/{token}/')
        self.assertEqual(dl.status_code, 200)
        self.assertEqual(dl['Content-Type'], 'application/pdf')
