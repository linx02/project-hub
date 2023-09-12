from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200, blank=False)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200, blank=False)
    image = CloudinaryField(blank=True, null=False, default='https://res.cloudinary.com/dyzoccovz/image/upload/v1694180826/cfdiszurokmzpvjxb5r9.png')
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_post')
    Category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='categories')
    created_on = models.DateField(auto_now_add=True)
    description = models.TextField()
    likes = models.ManyToManyField(User, related_name='liked_posts', null=True, blank=True)
    live_link = models.URLField(blank=True, null=True)
    github_repo_link = models.URLField(blank=True, null=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return self.title
    
    def number_of_likes(self):
        return self.likes.count()

class Comment(models.Model):
    body = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    created_on = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f'Comment {self.body} by {self.user}'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    github_profile_link = models.URLField(blank=True, null=True)