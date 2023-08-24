from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('project/<slug:slug>/', views.project_details, name='project_details'),
]