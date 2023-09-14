from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

def login_user(request):

    # Redirect home if user is already authenticated
    if request.user.is_authenticated:
        return redirect('home')

    # Runs on login
    if request.method == 'POST':

        # Authenticate user
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        # Login user and provide feedback
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('home')
        else:
            messages.success(request, 'There was an error logging in')
            return redirect('login')
    else:
        # Render login page
        return render(request, 'authenticate/login.html', {})

def logout_user(request):

    # Logout user and provide feedback
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('home')

def register_user(request):

    # Redirect home if user is already authenticated
    if request.user.is_authenticated:
        return redirect('home')
    
    # Runs on signup
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        # Check if form is valid
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            # Authenticate and login user
            user = authenticate(username=username, password=password)
            login(request, user)

            # Provide feedback
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        # Render sign up page and pass form
        form = UserCreationForm()

    return render(request, 'authenticate/signup.html', {'form':form})