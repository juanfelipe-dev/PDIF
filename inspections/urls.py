from django.urls import path
from . import views

app_name = 'inspections'

urlpatterns = [
    path('', views.landing, name='landing'),
    path('questionnaire/', views.questionnaire, name='questionnaire'),
    path('complete/<int:pk>/', views.completion, name='completion'),
    path('download/<str:token>/', views.download_pdf, name='download_pdf'),
]
