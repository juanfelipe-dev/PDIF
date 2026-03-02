from django.core.management.base import BaseCommand
from core.models import Organization
from inspections.models import Question


class Command(BaseCommand):
    help = 'Seed the database with a default organization and questions'

    def handle(self, *args, **options):
        org, created = Organization.objects.get_or_create(slug='default', defaults={'name': 'Default Organization'})
        if created:
            self.stdout.write(self.style.SUCCESS('Created default organization'))
        # No longer add sample questions to avoid duplicates
        pass
