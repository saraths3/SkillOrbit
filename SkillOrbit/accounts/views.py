from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from skill.models import UserSkill

# Create your views here.
# Registration

def signin_view(request):
    if request.method == 'POST':
        data = request.POST
        email = data.get('email')
        password = data.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            UserProfile.objects.get_or_create(user=user)
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('home') 
        else:
            messages.error(request, "Invalid email or password.")
            return render(request, 'accounts/signin.html', {'email': email, 'login_errors': True})
    return render(request, 'accounts/signin.html')

def signup_view(request):
    if request.method == 'POST':
        form = User_RegistrationForm(request.POST)
        full_name = request.POST.get('full_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not full_name or not full_name.strip():
            messages.error(request, 'Full name is required.')
            return render(request, 'accounts/signup.html', {'form': form})

        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'accounts/signup.html', {'form': form})

        if len(password1 or '') < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return render(request, 'accounts/signup.html', {'form': form})

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, f'{email} is already registered.')
            return render(request, 'accounts/signup.html', {'form': form})

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, f'Username "{username}" is already taken.')
            return render(request, 'accounts/signup.html', {'form': form})

        if form.is_valid():
            user = form.save()
            UserProfile.objects.get_or_create(user=user, defaults={'full_name': user.full_name})
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, 'Account created successfully!')
            return redirect('home')
        else:
            for field, errors in form.errors.items():
                for err in errors:
                    messages.error(request, f"{field.replace('_', ' ').title()}: {err}")
            return render(request, 'accounts/signup.html', {'form': form})
    else:
        form = User_RegistrationForm()

    return render(request, 'accounts/signup.html', {'form': form})

def forgot_password_view(request):
    if request.method == 'POST':
        data = request.POST
        email = data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            messages.success(request, 'Password reset instructions have been sent to your email.')
        else:
            messages.error(request, 'No user found with that email address.')
        return render(request, 'accounts/forgot_password.html')
    return render(request, 'accounts/forgot_password.html')

def reset_password_view(request):
    return render(request, 'accounts/reset_password.html')

def signout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('signin')

# Profile

@login_required(login_url="signin")
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user, defaults={'full_name': request.user.full_name})
    user_skills = UserSkill.objects.filter(user=request.user)
    context = {
        'profile': profile,
        "user_skills": user_skills,
    }
    return render(request, 'accounts/profile.html', context)


@login_required(login_url="signin")
def edit_profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user, defaults={'full_name': request.user.full_name})
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect("profile")
        else:
            messages.error(request, 'Failed to update profile. Please check the form.')
    else:
        form = UserProfileForm(instance=profile)
    context = {
        "form": form,
        "profile": profile,
    }
    return render(request, "accounts/edit_profile.html", context)
