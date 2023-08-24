from django.shortcuts import render
from .models import Category, Post

# Create your views here.

def home(request):
    context = {
        'posts' : Post.objects.all(),
        'categories' : Category.objects.all()
    }

    return render(request, 'index.html', context)