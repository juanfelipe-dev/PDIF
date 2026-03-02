import os
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Submission
from .utils import render_submission_pdf


@receiver(post_save, sender=Submission)
def generate_pdf(sender, instance, created, **kwargs):
    if created and not instance.pdf:
        try:
            path = render_submission_pdf(instance)
        except Exception as e:
            # log but don't prevent submission creation
            import logging
            logger = logging.getLogger(__name__)
            logger.exception("failed to render PDF for submission %s", instance.pk)
            return
        # save file to FileField
        from django.core.files import File
        with open(path, 'rb') as f:
            instance.pdf.save(os.path.basename(path), File(f), save=False)
        instance.compute_sha256(path)
        instance.save()
