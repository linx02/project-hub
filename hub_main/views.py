from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Post, Comment, User
from django.utils.text import slugify
from django.contrib import messages
from django.urls import reverse
from django.db.models import Count
import cloudinary.uploader
import os

# Create your views here.

def home(request):

    hof_posts = Post.objects.all().annotate(like_count=Count('likes'))
    hof_posts = hof_posts.order_by('-like_count')
    hof_posts = list(hof_posts)

    recent_posts = Post.objects.all().order_by('created_on')
    recent_posts = list(recent_posts)
    recent_posts.reverse()

    context = {
        'hof_post_1' : hof_posts[0],
        'hof_post_2' : hof_posts[1],
        'hof_post_3' : hof_posts[2],
        'recent_posts' : recent_posts[:4],
        'categories' : Category.objects.all()
    }

    return render(request, 'index.html', context)

def project_details(request, slug):

    post = get_object_or_404(Post.objects.all(), slug=slug)
    comments = post.comments.all().order_by('created_on')
    liked = False
    author_posts = Post.objects.filter(author=post.author)
    if post.likes.filter(id=request.user.id).exists():
        liked = True

    context = {
        'post' : post,
        'comments' : comments,
        'liked' : liked,
        'author' : post.author,
        'author_posts' : author_posts[:4]
    }

    return render(request, 'project_details.html', context)

def project_submission(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        slug = slugify(title)

        if 'generate_link' in request.POST:
            image_file = f'https://image.thum.io/get/width/1600/crop/700/auth/{os.environ.get("THUMIO_AUTH")}/{request.POST["live_link"]}'

        else:
            image_file = request.FILES.get('image')

        upload_result = cloudinary.uploader.upload(image_file)
        
        posts_table = Post(title=request.POST['title'],
                           author=request.user,
                           Category_id=request.POST['category'],
                           description=request.POST['description'],
                           image=upload_result['secure_url'],
                           live_link=request.POST['live_link'],
                           github_repo_link=request.POST['github_repo_link'],
                           slug=slug)
        posts_table.save()

        messages.success(request, 'Your project has been posted. Thank you for your submission!')
        return redirect('profile_page')
    else:
        return render(request, 'project_submission.html')

def project_update(request, post_id):
    post_to_update = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        title = request.POST.get('title')
        slug = slugify(title)


        post_to_update.title=title
        post_to_update.Category_id=request.POST.get('category')
        post_to_update.description=request.POST.get('description')

        
        image_file = request.FILES.get('image')
        print(image_file)
        upload_result = cloudinary.uploader.upload(image_file)

        post_to_update.image=upload_result['secure_url']
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

    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post has been deleted')
    
    return redirect('profile_page')

def post_comment(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        
        comment = Comment(
            body=request.POST['comment_body'],
            user=request.user,
            post=post
        )

        comment.save()
        messages.success(request, 'Your comment has been posted.')

        redirect_url = reverse('project_details', kwargs={'slug': post.slug})
        return redirect(redirect_url)
    
def delete_comment(request, comment_id, post_id):
    comment = get_object_or_404(Comment, id=comment_id)
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Comment has been deleted')

        redirect_url = reverse('project_details', kwargs={'slug': post.slug})
        return redirect(redirect_url)

    
def browse_project(request, pp, sort_by):
    
    if sort_by == 'a-z':
        posts = Post.objects.all().order_by('title')
        posts = list(posts)
        posts.reverse()
        return render(request, 'browse_project.html', {'posts': Post.objects.filter(Category_id=pp).order_by('title'), 'category' : Category.objects.get(id=pp)})
    elif sort_by == 'recently-added':
        posts = Post.objects.filter(Category_id=pp).order_by('-created_on')
        posts = list(posts)
        posts.reverse()
        context = {
            'posts' : posts,
            'category' : Category.objects.get(id=pp)
        }

        return render(request, 'browse_project.html', context)

    elif sort_by == 'top-rated':
        posts = Post.objects.filter(Category_id=pp).annotate(like_count=Count('likes'))
        posts = posts.order_by('-like_count')
        context = {
            'posts' : posts,
            'category' : Category.objects.get(id=pp)
        }

        return render(request, 'browse_project.html', {'posts': posts, 'category' : Category.objects.get(id=pp)})
    
    else:
        return render(request, 'browse_project.html', {'posts': Post.objects.filter(Category_id=pp), 'category' : Category.objects.get(id=pp)})


def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    redirect_url = reverse('project_details', kwargs={'slug': post.slug})
    return redirect(redirect_url)

def view_profile(request, username):
    profile = get_object_or_404(User, username=username)
    context = {
        'profile' : profile,
        'posts' : Post.objects.filter(author=profile),
        'post_count' : Post.objects.filter(author=profile).count(),
    }

    return render(request, 'view_profile.html', context)

def custom_404_page(request, *args, **kwargs):
    return render(request, '404.html', status=404)