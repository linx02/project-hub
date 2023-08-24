from django.shortcuts import render, get_object_or_404
from .models import Category, Post

# Create your views here.

def home(request):
    context = {
        'posts' : Post.objects.all(),
        'categories' : Category.objects.all()
    }

    return render(request, 'index.html', context)

def project_details(request, slug):

    post = get_object_or_404(Post.objects.all(), slug=slug)
    comments = post.comments.all().order_by('created_on')
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        liked = True
    
    context = {
        'post' : post,
        'comments' : comments,
        'liked' : liked,
        'author' : post.author
    }

    return render(request, 'project_details.html', context)