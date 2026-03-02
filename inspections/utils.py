from django.template.loader import render_to_string
from django.conf import settings
import os

# weasyprint has native dependencies that may not be available during CLI
# operations such as makemigrations. import inside function to avoid errors.
try:
    from weasyprint import HTML
except (ImportError, OSError):
    # weasyprint may raise OSError when native libs missing (e.g. libgobject)
    HTML = None

def render_submission_pdf(submission):
    """Render the PDF for a Submission object and return the file path.

    We first try to use WeasyPrint (HTML). If it's not available we fall back to a
    very simple ReportLab implementation to avoid crashing in environments where
    the full dependencies cannot be installed (e.g. CI, Windows dev).
    """
    output_dir = os.path.join(settings.MEDIA_ROOT, 'generated_pdfs')
    os.makedirs(output_dir, exist_ok=True)
    filename = f"submission_{submission.id}.pdf"
    output_path = os.path.join(output_dir, filename)

    if HTML is not None:
        # template should exist at inspections/pdf/submission.html
        branding = None
        try:
            branding = submission.organization.branding
        except Exception:
            branding = None
        html_string = render_to_string('inspections/pdf/submission.html', {
            'submission': submission,
            'branding': branding,
        })
        HTML(string=html_string, base_url=settings.BASE_DIR).write_pdf(output_path)
        return output_path

    # fallback using reportlab
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
    except ImportError:
        raise ImportError("No PDF library available to render submission")

    c = canvas.Canvas(output_path, pagesize=letter)
    text = c.beginText(40, 750)
    text.setFont("Helvetica-Bold", 14)
    text.textLine("Inspection Report")
    text.setFont("Helvetica", 10)
    text.textLine(f"Organization: {submission.organization.name}")
    text.textLine(f"Date: {submission.created_at}")
    text.textLine(" ")
    for key, value in submission.data.items():
        text.setFont("Helvetica-Bold", 12)
        text.textLine(str(key))
        text.setFont("Helvetica", 10)
        text.textLine(str(value))
        text.textLine(" ")
    c.drawText(text)
    c.showPage()
    c.save()
    return output_path
