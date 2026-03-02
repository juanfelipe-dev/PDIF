from .models import Organization
from branding.models import Branding

def current_organization(request):
    org = Organization.objects.first()
    branding = None
    if org:
        try:
            branding = org.branding
        except Branding.DoesNotExist:
            branding = None
    return {
        'current_org': org,
        'branding': branding,
    }
