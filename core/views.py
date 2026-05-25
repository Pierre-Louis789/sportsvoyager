from django.shortcuts import render, get_object_or_404, redirect
from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Pack, UnlockedPack


def home(request):
    featured = Pack.objects.all().order_by('-created_at')[:3]  # latest 3 packs
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

    unlocked = False
    if request.user.is_authenticated:
        unlocked = UnlockedPack.objects.filter(user=request.user, pack=pack).exists()

    return render(request, 'packs/pack_detail.html', {
        'pack': pack,
        'unlocked': unlocked
    })


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'auth/register.html', {'form': form})


@login_required
def unlock_pack(request, pk):
    pack = get_object_or_404(Pack, pk=pk)

    # Create unlock record if not exists
    UnlockedPack.objects.get_or_create(user=request.user, pack=pack)

    return redirect('pack_detail', pk=pk)

def my_packs(request):
    unlocked = UnlockedPack.objects.filter(user=request.user).select_related('pack')
    return render(request, 'packs/my_packs.html', {'unlocked': unlocked})