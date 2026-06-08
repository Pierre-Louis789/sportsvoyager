from django.shortcuts import render, get_object_or_404, redirect
from django.db import models
from django.contrib.auth.decorators import login_required

from .forms import CustomRegisterForm, CommentForm
from .models import UserProfile, Pack, UnlockedPack, Comment


def home(request):
    featured = Pack.objects.all()[:3]
    return render(request, 'home.html', {'featured': featured})


def pack_list(request):
    query = request.GET.get('q', '')

    if query:
        packs = Pack.objects.filter(
            models.Q(title__icontains=query) |
            models.Q(club__icontains=query) |
            models.Q(league__icontains=query) |
            models.Q(description__icontains=query)
        ).order_by('-created_at')
    else:
        packs = Pack.objects.all().order_by('-created_at')

    return render(request, 'packs/pack_list.html', {
        'packs': packs,
        'query': query
    })


def pack_detail(request, pk):
    pack = get_object_or_404(Pack, pk=pk)
    comments = pack.comments.all()

    # Handle comment POST
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect('login')

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.pack = pack
            comment.user = request.user
            comment.save()
            return redirect('pack_detail', pk=pk)
    else:
        form = CommentForm()

    # Check if pack is unlocked
    unlocked = False
    if request.user.is_authenticated:
        unlocked = UnlockedPack.objects.filter(user=request.user, pack=pack).exists()

    return render(request, 'packs/pack_detail.html', {
        'pack': pack,
        'comments': comments,
        'form': form,
        'unlocked': unlocked,
    })


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
def unlock_pack(request, pk):
    pack = get_object_or_404(Pack, pk=pk)
    UnlockedPack.objects.get_or_create(user=request.user, pack=pack)
    return redirect('pack_detail', pk=pk)


def my_packs(request):
    unlocked = UnlockedPack.objects.filter(user=request.user).select_related('pack')
    return render(request, 'packs/my_packs.html', {'unlocked': unlocked})


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
