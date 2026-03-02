from django.contrib import admin
from .models import Question, Submission


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('organization','text','sort_order')
    list_filter = ('organization',)


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('id','organization','created_at','pdf')
    list_filter = ('organization',)
    readonly_fields = ('pdf_sha256',)
