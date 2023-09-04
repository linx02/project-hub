from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Post
from django.utils.text import slugify
from django.contrib import messages

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

        messages.success(request, 'Post successful. Thank you for your submission!')
        return redirect('profile_page')
    else:
        return render(request, 'project_submission.html')
    
def profile_page(request):
    context = {
        'posts' : Post.objects.filter(author=request.user),
        'post_count' : Post.objects.filter(author=request.user).count(),
    }
    
    return render(request, 'profile_page.html', context)

def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        post.delete()
        messages.success(request, 'Post has been deleted')
    
    return redirect('profile_page')