# PDIF Inspection

This Django project implements a multi-tenant inspection platform with automatic PDF generation and white-label branding. It is designed to be an institutional/hospital-grade SaaS.

## Features

- Organizations (tenants) managed via Django admin
- Config-driven question list
- Submission storage with JSON data
- Individual PDF generation per submission (WeasyPrint or fallback ReportLab)
- SHA256 checksum recorded on each PDF
- White-label branding (logo, primary color, footer resources)
- Clean public UI (landing page, questionnaire, completion)
- Mobile-responsive Bootstrap styling

## Setup

1. Create virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   .venv\\Scripts\\activate  # Windows Powershell
   pip install -r requirements.txt
   ```
   *Note:* the project uses WeasyPrint which requires native libraries (`libgobject`, `cairo`, etc.). On Windows these are not installed by default; we use a ReportLab fallback for development.

2. (Optional) load sample submission data
   ```bash
   # sample JSON included in tests/sample_submission.json
   cat tests/sample_submission.json
   ```

## Running Tests

Automated tests cover model behaviors and key views. Execute via:
```bash
python manage.py test inspections
```
A successful run will create an organization, submit answers, generate a PDF, and verify the secure download link.


2. Apply migrations:
   ```bash
   python manage.py migrate
   python manage.py seed  # add sample org and questions
   ```

3. Collect static files for production (this is required for Render and for local static serving via WhiteNoise):
   ```bash
   python manage.py collectstatic --noinput
   ```

> We use [WhiteNoise](http://whitenoise.evans.io/) to serve static assets directly from Django when running on Render or other platforms without a dedicated CDN. The middleware is already configured in `settings.py`.

4. Run development server:
   ```bash
   python manage.py runserver
   ```

## Creating an Organization

1. Log in to the Django admin at `/admin/` (create a superuser via `createsuperuser`).
2. Add an `Organization` instance. The `slug` will be used for tenant identification.
3. Optionally create a `Branding` object linked to the organization: upload a logo, set a primary color (hex), enable footer and add resources text.
4. Add `Question` objects for that organization; use `sort_order` to control sequence.

## Branding Setup

- `logo` will be shown in the header.
- `primary_color` applies to navigation background.
- `footer_enabled`: when checked, the `resources_text` is rendered at page footers instead of default footer.
- Color and logo also influence the generated PDF (PDF template can be extended to inject branding assets).

## PDF Generation Details

- Each `Submission` triggers a post-save signal generating a PDF file.
- The PDF is saved under `MEDIA_ROOT/generated_pdfs/` and attached to the `Submission.pdf` field.
- The SHA256 hash of the file is computed and stored in `pdf_sha256`.
- If WeasyPrint cannot be imported (missing native libs), a fallback with ReportLab creates a simple text-based PDF.

## Design mockup & PDF preview

Before implementing layout changes, a visual mock should be reviewed. The current templates emphasize a neutral, clinical tone – white backgrounds, generous margins, serif headers and clean sans-serif body text. Requirements for design include:

- **Tone:** neutral, clinical, inspection-style; avoid emotional language.
- **Visual system:** white background, generous margins, serif header font, clean sans-serif body.
- **Color palette:** muted system colors for statuses:
  - **Cleared:** soft green
  - **Watch:** amber
  - **Elevated:** muted red
- **Indicators:** horizontal bars convey status and separate sections.
- **Scope & limitations:** final page includes a concise statement.

These elements are implemented in templates and CSS (`static/css/pdif.css`), with bar classes `.bar.cleared`, `.bar.watch`, and `.bar.elevated`.

A sample rendered report is available in the repository:

- [docs/sample_report.pdf](docs/sample_report.pdf)

This file demonstrates the clinical inspection‑style layout and can be opened directly for review. Adjustments should be approved before further implementation.

## Deployment (Render)

1. Push repository to GitHub.
2. Create a new Web Service on Render using the `python` environment.
3. Set build command: `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput`
4. Set start command: `gunicorn pdif_project.wsgi` (or use `python manage.py runserver 0.0.0.0:10000` for testing).
5. Configure environment variables:
   - `DJANGO_SECRET_KEY` (override secret)
   - `DEBUG=False`
   - `ALLOWED_HOSTS` (e.g. `['*']` or your domain)
   - `DATABASE_URL` (Render managed Postgres)
   - `MEDIA_ROOT` and `STATIC_ROOT` to suitable directories or S3.
6. Add `django_heroku` or adjust settings for static/media, CORS, etc.

Verify public UI works and PDF generation produces correct files with SHA.

## Notes

- The current multi-tenant logic simply picks the first organization. To extend, resolve the tenant via request host or path.
- For white-labeling full UI and PDF, extend templates to reference `branding` context and apply CSS classes/style blocks.
- Additional features like configuration versioning, rules engine, or aggregated PDFs can be built on top of this core.

---
