from django.db import models

from core.models import Organization


class Branding(models.Model):
    organization = models.OneToOneField(Organization, on_delete=models.CASCADE)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    primary_color = models.CharField(max_length=7, blank=True, help_text='Hex color code, e.g. #1a2b3c')
    footer_enabled = models.BooleanField(default=False)
    resources_text = models.TextField(blank=True)

    def __str__(self):
        return f"Branding for {self.organization}"
