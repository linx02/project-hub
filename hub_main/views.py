from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Post
from django.utils.text import slugify

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

def project_submission(request):
    if request.method == "POST":
        title = request.POST.get('title', '')
        slug = slugify(title)
        
        posts_table = Post(title=request.POST['title'],
                           author=request.user,
                           Category_id=request.POST['category'],
                           description=request.POST['description'],
                           live_link=request.POST['live_link'],
                           github_repo_link=request.POST['github_repo_link'],
                           slug=slug)
        posts_table.save()

        return redirect('home')
    else:
        return render(request, 'project_submission.html')