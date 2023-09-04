from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('project/<slug:slug>/', views.project_details, name='project_details'),
    path('project_submission/', views.project_submission, name='project_submission'),
    path('profile_page/', views.profile_page, name='profile_page'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('project_update/<int:post_id>/', views.project_update, name="project_update")
]