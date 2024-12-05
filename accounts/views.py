from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  # Log in the user
            return redirect('index')  # Redirect to the index page
        else:
            return HttpResponse("Invalid username or password!")

    return render(request, 'login.html')  # Render login page if GET request

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Check if passwords match
        if password1 != password2:
            return HttpResponse("Passwords do not match!")
        
        # Create the user
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        
        return redirect('login')  # Redirect to login page after signup
    return render(request, 'signup.html')  # Render signup page if GET request


@login_required(login_url='login')  # Ensure the user is logged in
def index_view(request):
    # Check if the logged-in user is a superuser
    if not request.user.is_superuser:
        return HttpResponseForbidden("You are not authorized to access this page.")
    
    # If the user is a superuser, proceed to render the index page
    superusers = User.objects.filter(is_superuser=True)
    users = [
        {
            'username': user.username,
            'email': user.email,
            'role': 'Admin' if user.is_superuser else 'User',
            'date_time': user.last_login if user.last_login else "no history available"
        }
        for user in User.objects.all()
    ]

    superuser_username = superusers[0].username if superusers.exists() else "No Superadmin Found"

    context = {
        'superuser_username': superuser_username,
        'users': users,
    }
    return render(request, 'index.html', context)


def logout_view(request):
    logout(request)  # Log out the user
    return redirect('login')  # Redirect to the login 

def delete_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.delete()
        return HttpResponse(f"User {user.username} deleted successfully.")
    except User.DoesNotExist:
        return HttpResponse("User not found.", status=404)    

@login_required
def delete_user_view(request, user_id):
    user_to_delete = get_object_or_404(User, id=user_id)

    # Prevent deletion of superusers
    if user_to_delete.is_superuser:
        return HttpResponseForbidden("You cannot delete a superuser.")

    user_to_delete.delete()
    return redirect('index')
    