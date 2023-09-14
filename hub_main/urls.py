from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'), # Home path
    path('project/<slug:slug>/', views.project_details, name='project_details'), # Project path
    path('project_submission/', views.project_submission, name='project_submission'), # Project submission path
    path('profile_page/', views.profile_page, name='profile_page'), # Users profile page path
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'), # Delete post path
    path('project_update/<int:post_id>/', views.project_update, name='project_update'), # Update project path
    path('post_comment/<int:post_id>/', views.post_comment, name='post_comment'), # Post comment path
    path('delete_comment/<int:comment_id>/<int:post_id>/', views.delete_comment, name='delete_comment'), # Delete comment path
    path('browse_project/<int:pp>/<str:sort_by>/', views.browse_project, name='browse_project'), # Browse projects path
    path('like_post/<int:post_id>/', views.like_post, name='like_post'), # Like post path
    path('profile/<str:username>/', views.view_profile, name='view_profile'), # Profile page path
    path('404/', views.custom_404_page, name='custom_404_page'), # 404 path
]