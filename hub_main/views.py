from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Post
from django.utils.text import slugify
from django.contrib import messages

# Create your views here.

def home(request):
    recent_posts = Post.objects.all().order_by('created_on')
    recent_posts = list(recent_posts)
    recent_posts.reverse()
    context = {
        'posts' : recent_posts[:4],
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
        title = request.POST.get('title')
        slug = slugify(title)
        
        posts_table = Post(title=request.POST['title'],
                           author=request.user,
                           Category_id=request.POST['category'],
                           description=request.POST['description'],
                           live_link=request.POST['live_link'],
                           github_repo_link=request.POST['github_repo_link'],
                           slug=slug)
        posts_table.save()

        messages.success(request, 'Your project has been posted. Thank you for your submission!')
        return redirect('profile_page')
    else:
        return render(request, 'project_submission.html')

def project_update(request, post_id):
    post_to_update = Post.objects.get(id=post_id)

    if request.method == "POST":
        title = request.POST.get('title')
        slug = slugify(title)


        post_to_update.title=title
        post_to_update.Category_id=request.POST.get('category')
        post_to_update.description=request.POST.get('description')
        post_to_update.live_link=request.POST.get('live_link')
        post_to_update.github_repo_link=request.POST.get('github_repo_link')
        post_to_update.slug=slug

        post_to_update.save()

        messages.success(request, 'Post has been updated.')
        return redirect('profile_page')
    
    else:
        context = {
            'title': post_to_update.title,
            'category': post_to_update.Category_id,
            'description': post_to_update.description,
            'live_link': post_to_update.live_link,
            'github_repo_link': post_to_update.github_repo_link,
            'post_id': post_to_update.id
        }

        return render(request, 'project_update.html', context)

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