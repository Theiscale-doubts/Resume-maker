from django.urls import path
from . import views

urlpatterns = [
    path('generate-summary/', views.generate_summary, name='generate_summary'),
    path('enhance-description/', views.enhance_description, name='enhance_description'),
    path('analyze-resume/', views.analyze_resume, name='analyze_resume'),
]
