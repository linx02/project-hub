from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Post, Comment, User
from django.utils.text import slugify
from django.contrib import messages
from django.urls import reverse
from django.db.models import Count
from django.core.paginator import Paginator
import cloudinary.uploader
import os


def home(request):

    # Get posts for hall of fame sections
    hof_posts = Post.objects.all().annotate(like_count=Count('likes'))
    hof_posts = hof_posts.order_by('-like_count')
    hof_posts = list(hof_posts)

    # Get posts for recently added section
    recent_posts = Post.objects.all().order_by('created_on')
    recent_posts = list(recent_posts)
    recent_posts.reverse()

    # Context to be passed
    context = {
        'hof_post_1': hof_posts[0],
        'hof_post_2': hof_posts[1],
        'hof_post_3': hof_posts[2],
        'recent_posts': recent_posts[:4],
        'categories': Category.objects.all()
    }

    return render(request, 'index.html', context)


def project_details(request, slug):

    # Get post to be viewed
    post = get_object_or_404(Post.objects.all(), slug=slug)

    # Get comments for post
    comments = post.comments.all().order_by('created_on')

    # Get user liked status
    liked = False
    author_posts = Post.objects.filter(author=post.author)
    if post.likes.filter(id=request.user.id).exists():
        liked = True

    # Context to be passed
    context = {
        'post': post,
        'comments': comments,
        'liked': liked,
        'author': post.author,
        'author_posts': author_posts[:4]
    }

    return render(request, 'project_details.html', context)


def project_submission(request):

    # Redirect home if user is not authenticated
    if not request.user.is_authenticated:
        return redirect('home')

    # Runs on submission
    if request.method == 'POST':

        # Get title and generate slug
        title = request.POST.get('title')
        slug = slugify(title)

        # Generate screenshot if 'Generate from link' button is toggled
        if 'generate_link' in request.POST:
            image_file = f'https://image.thum.io/get/width/1600/crop/700/auth/{os.environ.get("THUMIO_AUTH")}/{request.POST["live_link"]}'
            upload_result = cloudinary.uploader.upload(image_file)
            image = upload_result['secure_url']

        # Get file if file was uploaded
        elif request.FILES:
            image_file = request.FILES.get('image')
            upload_result = cloudinary.uploader.upload(image_file)
            image = upload_result['secure_url']

        # Use default image if none was provided
        else:
            image = None

        # Create and save post in db
        posts_table = Post(title=request.POST['title'],
                           author=request.user,
                           Category_id=request.POST['category'],
                           description=request.POST['description'],
                           image=image,
                           live_link=request.POST['live_link'],
                           github_repo_link=request.POST['github_repo_link'],
                           slug=slug)
        posts_table.save()

        # Provide feedback to user
        messages.success(request, 'Your project has been posted. Thank you for your submission!')
        return redirect('profile_page')
    else:
        # Provide form
        return render(request, 'project_submission.html')


def project_update(request, post_id):

    # Redirect home if user is not authenticated
    if not request.user.is_authenticated:
        return redirect('home')

    # Get post to update
    post_to_update = get_object_or_404(Post, id=post_id)

    # Redirect home if user is not author of post
    if post_to_update.author != request.user:
        return redirect('home')

    # Runs on submission
    if request.method == 'POST':

        # Get new title and generate new slug
        title = request.POST.get('title')
        slug = slugify(title)

        # Get new data
        post_to_update.title = title
        post_to_update.Category_id = request.POST.get('category')
        post_to_update.description = request.POST.get('description')

        # Handle 'Generate from link' button toggled
        if 'generate_link' in request.POST:
            image_file = f'https://image.thum.io/get/width/1600/crop/700/auth/{os.environ.get("THUMIO_AUTH")}/{request.POST["live_link"]}'
            upload_result = cloudinary.uploader.upload(image_file)
            image = upload_result['secure_url']

        # Handle file uploaded
        elif request.FILES:
            image_file = request.FILES.get('image')
            upload_result = cloudinary.uploader.upload(image_file)
            image = upload_result['secure_url']

        # Handle none provided
        else:
            image = None

        # Create new record and save to db
        post_to_update.image = image
        post_to_update.live_link = request.POST.get('live_link')
        post_to_update.github_repo_link = request.POST.get('github_repo_link')
        post_to_update.slug = slug

        post_to_update.save()

        # Provide user feedback
        messages.success(request, 'Post has been updated.')
        return redirect('profile_page')

    else:
        # Provide data to be pre-filled to inputs when accessing page
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

    # Redirect home if user is not authenticated
    if not request.user.is_authenticated:
        return redirect('home')

    # Context to be passed
    context = {
        'posts': Post.objects.filter(author=request.user),
        'post_count': Post.objects.filter(author=request.user).count(),
    }

    return render(request, 'profile_page.html', context)


def delete_post(request, post_id):

    # Redirect home if user is not authenticated
    if not request.user.is_authenticated:
        return redirect('home')

    # Get post to delete
    post = get_object_or_404(Post, id=post_id)

    # Redirect home if user is not author of post
    if post.author != request.user:
        return redirect('home')

    # Delete post and provide user feedback
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post has been deleted')

    return redirect('profile_page')


def post_comment(request, post_id):

    # Redirect home if user is not authenticated
    if not request.user.is_authenticated:
        return redirect('home')

    # Runs on submission
    if request.method == 'POST':

        # Get post to be commented on
        post = get_object_or_404(Post, id=post_id)

        # Deny if comment is empty
        if request.POST.get('comment_body').strip() == '':
            messages.success(request, 'Empty comments not allowed')

            redirect_url = reverse('project_details', kwargs={'slug': post.slug})
            return redirect(redirect_url)

        # Create record, save to db and provide user feedback
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

    # Redirect home if user is not authenticated
    if not request.user.is_authenticated:
        return redirect('home')

    # Get comment to be deleted, post to redirect to when done
    comment = get_object_or_404(Comment, id=comment_id)
    post = get_object_or_404(Post, id=post_id)

    # Redirect home if user is not author of comment
    if comment.user != request.user:
        return redirect('home')

    # Delete comment and provide user feedback
    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Comment has been deleted')

        redirect_url = reverse('project_details', kwargs={'slug': post.slug})
        return redirect(redirect_url)


def browse_project(request, pp, sort_by):

    # Get category
    category = Category.objects.get(id=pp)

    # Handle pagination
    def paginate(all_posts):
        p = Paginator(all_posts, 12)
        page = request.GET.get('page')
        posts = p.get_page(page)
        return posts

    # Handle sort by a-z
    if sort_by == 'a-z':
        all_posts = Post.objects.filter(Category_id=pp).order_by('title')

        posts = paginate(all_posts)

        return render(request, 'browse_project.html', {'posts': posts, 'category': category})

    # Handle sort by recently added
    elif sort_by == 'recently-added':
        all_posts = Post.objects.filter(Category_id=pp).order_by('-created_on')

        posts = paginate(all_posts)

        context = {
            'posts': posts,
            'category': category
        }

        return render(request, 'browse_project.html', context)

    # Handle sort by top rated
    elif sort_by == 'top-rated':
        all_posts = Post.objects.filter(Category_id=pp).annotate(like_count=Count('likes'))
        all_posts = all_posts.order_by('-like_count')

        posts = paginate(all_posts)

        context = {
            'posts': posts,
            'category': category
        }

        return render(request, 'browse_project.html', {'posts': posts, 'category': category})

    # Render page
    else:
        all_posts = Post.objects.filter(Category_id=pp)
        posts = paginate(all_posts)
        return render(request, 'browse_project.html', {'posts': posts, 'category': category})


def like_post(request, post_id):

    # Redirect home if user is not authenticated
    if not request.user.is_authenticated:
        return redirect('home')

    # Get post to like
    post = get_object_or_404(Post, id=post_id)

    # Like if not liked, unlike if already liked
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    # Render project page
    redirect_url = reverse('project_details', kwargs={'slug': post.slug})
    return redirect(redirect_url)


def view_profile(request, username):

    # Get profile to view
    profile = get_object_or_404(User, username=username)

    # Context to be passed
    context = {
        'profile': profile,
        'posts': Post.objects.filter(author=profile),
        'post_count': Post.objects.filter(author=profile).count(),
    }

    # Render page
    return render(request, 'view_profile.html', context)


def custom_404_page(request, *args, **kwargs):

    # Render custom 404 page
    return render(request, '404.html', status=404)
