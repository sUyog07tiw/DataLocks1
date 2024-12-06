from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_control
from django.utils import timezone
import re
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


@csrf_exempt
def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('index')  # Redirect to the admin dashboard
        return render(request, 'base')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            user.last_login = timezone.now()  # Update last login time
            user.save()   # Log in the user

            # Redirect based on user type
            if user.is_superuser:
                return redirect('index')  # Redirect to index page for superadmins
            else:
                return redirect('base')  # Redirect to base page for regular users

        else:
            return HttpResponse("Invalid username or password!")

    return render(request, 'login.html') # Render the login page


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def signup_view(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('index')  # Redirect to the admin dashboard
        return redirect('base')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Check if passwords match
        if password1 != password2:
            return HttpResponse("Passwords do not match!")

        # Check password validation rules
        if len(password1) > 8:
            return HttpResponse("Password must not exceed 8 characters.")
        
        # Check for at least one uppercase letter, one symbol, and max 8 characters
        if not re.search(r'[A-Z]', password1):
            return HttpResponse("Password must contain at least one uppercase letter.")
        
        if not re.search(r'[\W_]', password1):  # \W matches any non-word character (including symbols)
            return HttpResponse("Password must contain at least one symbol.")
        
        # Validate the email address
        try:
            validate_email(email)  # Validate the email format
        except ValidationError:
            return HttpResponse("Invalid email address.")
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            return HttpResponse("This email address is already taken.")
        
        # Create the user
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        
        return redirect('login')  # Redirect to login page after signup
    return render(request, 'signup.html')  # Render signup page if GET request  # Render signup page if GET request

 # Ensure the user is logged in
@login_required(login_url='login')  # Ensure the user is logged in
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index_view(request):
    # Check if the logged-in user is a superuser
    if not request.user.is_superuser:
        
        return render(request, 'base.html')
    

    # Proceed if the user is a superuser
    superusers = User.objects.filter(is_superuser=True)
    users = [
        {
            'username': user.username,
            'email': user.email,
            'role': 'Admin' if user.is_superuser else 'User',
            'date_time': user.last_login if user.last_login else "no history available",
            'delete_url': reverse('delete_user', args=[user.id])
        }
        for user in User.objects.all()
    ]

    superuser_username = superusers[0].username if superusers.exists() else "No Superadmin Found"

    context = {
        'superuser_username': superuser_username,
        'users': users,
    }
    return render(request, 'index.html', context)

@login_required(login_url='login')  # Ensure the user is logged in
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def base_view(request):
    return render(request, 'base.html')  

@login_required
def delete_user_view(request, user_id):
    user_to_delete = get_object_or_404(User, id=user_id)

    # Prevent deletion of superusers
    if user_to_delete.is_superuser:
        return HttpResponseForbidden("You cannot delete a superuser.")

    user_to_delete.delete()
    return redirect('index')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout_view(request):
    logout(request)
    # Clear the session completely
    request.session.flush()
    return redirect('login')  # Redirect to the login 
   
def browse_jobs(request):
    return render(request, 'jobs')

