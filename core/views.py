from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import CustomRegisterForm
from .models import UserProfile


def home(request):
    from packs.models import Pack
    featured = Pack.objects.all()[:3]
    return render(request, 'home.html', {'featured': featured})


def register(request):
    if request.method == "POST":
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomRegisterForm()

    return render(request, 'auth/register.html', {'form': form})


@login_required
def profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'profile/profile.html', {'profile': profile})


@login_required
def profile_edit(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        profile.favourite_team = request.POST.get('favourite_team')
        profile.country = request.POST.get('country')
        profile.bio = request.POST.get('bio')

        if 'avatar' in request.FILES:
            profile.avatar = request.FILES['avatar']

        profile.save()
        return redirect('profile')

    return render(request, 'profile/profile_edit.html', {'profile': profile})
