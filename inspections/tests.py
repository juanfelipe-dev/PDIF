from django.test import TestCase
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
