import hashlib
from django.db import models
from django.urls import reverse

from core.models import Organization


class Question(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    text = models.TextField()
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['sort_order']

    def __str__(self):
        return f"Q{self.sort_order}: {self.text[:40]}"


class Submission(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    pdf = models.FileField(upload_to='submissions_pdfs/', blank=True, null=True)
    pdf_sha256 = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return f"Submission {self.id} for {self.organization}"

    def get_absolute_url(self):
        return reverse('inspections:completion', kwargs={'pk': self.pk})

    def compute_sha256(self, file_path):
        sha = hashlib.sha256()
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                sha.update(chunk)
        self.pdf_sha256 = sha.hexdigest()
        self.save()
