from django.core.management.base import BaseCommand
from core.models import Organization
from inspections.models import Question


class Command(BaseCommand):
    help = 'Seed the database with a default organization and questions'

    def handle(self, *args, **options):
        org, created = Organization.objects.get_or_create(slug='default', defaults={'name': 'Default Organization'})
        if created:
            self.stdout.write(self.style.SUCCESS('Created default organization'))
        # add a few sample questions
        if not Question.objects.filter(organization=org).exists():
            Question.objects.create(organization=org, text='Describe the facility cleanliness', sort_order=1)
            Question.objects.create(organization=org, text='List any safety hazards observed', sort_order=2)
            self.stdout.write(self.style.SUCCESS('Added sample questions'))
        else:
            self.stdout.write('Questions already present')
