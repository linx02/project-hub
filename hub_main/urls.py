from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('project/<slug:slug>/', views.project_details, name='project_details'),
    path('project_submission/', views.project_submission, name='project_submission'),
    path('profile_page/', views.profile_page, name='profile_page'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('project_update/<int:post_id>/', views.project_update, name='project_update'),
    path('post_comment/<int:post_id>/', views.post_comment, name='post_comment'),
    path('delete_comment/<int:comment_id>/<int:post_id>/', views.delete_comment, name='delete_comment'),
    path('browse_project/<int:pp>/<str:sort_by>/', views.browse_project, name='browse_project'),
    path('like_post/<int:post_id>/', views.like_post, name='like_post'),
    path('profile/<str:username>/', views.view_profile, name='view_profile')
]