from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.core import signing
from django.http import HttpResponse, Http404

from core.models import Organization
from .models import Question, Submission


def landing(request):
    return render(request, 'inspections/landing.html')


def questionnaire(request):
    # in a real multi-tenant app, determine organization by hostname or path
    org = Organization.objects.first()
    if request.method == 'POST':
        data = {k: v for k, v in request.POST.items() if k.startswith('q_')}
        submission = Submission.objects.create(organization=org, data=data)
        return redirect('inspections:completion', pk=submission.pk)
    questions = Question.objects.filter(organization=org)
    return render(request, 'inspections/questionnaire.html', {'questions': questions})


def completion(request, pk):
    submission = get_object_or_404(Submission, pk=pk)
    # generate signed token for download link
    token = signing.dumps({'submission_id': submission.pk})
    return render(request, 'inspections/completion.html', {'submission': submission, 'download_token': token})


def download_pdf(request, token):
    try:
        data = signing.loads(token, max_age=60 * 60 * 24)  # 1 day validity
        sid = data.get('submission_id')
    except signing.BadSignature:
        raise Http404("Invalid download link")
    submission = get_object_or_404(Submission, pk=sid)
    if not submission.pdf:
        raise Http404("No PDF available")
    # stream file
    response = HttpResponse(submission.pdf.open('rb').read(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{submission.pdf.name.split("/")[-1]}"'
    return response
