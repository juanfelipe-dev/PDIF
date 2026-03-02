import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE','pdif_project.settings')
django.setup()
from core.models import Organization
from inspections.models import Submission

org = Organization.objects.first()
data={'q_1':'Answer1','q_2':'Answer2'}
sub = Submission.objects.create(organization=org, data=data)
print('created', sub.id, sub.pdf, sub.pdf_sha256)
