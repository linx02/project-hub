from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('project/<slug:slug>/', views.project_details, name='project_details'),
    path('project_submission/', views.project_submission, name='project_submission')
]