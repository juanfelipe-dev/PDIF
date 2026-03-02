from django.db import models


class Organization(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    # optional contact/description fields could go here

    def __str__(self):
        return self.name
