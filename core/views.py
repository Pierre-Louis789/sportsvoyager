from django.shortcuts import render, get_object_or_404, redirect
from django.db import models
from .models import Pack

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

    return render(request, 'pack_list.html', {
        'packs': packs,
        'query': query
    })


def pack_detail(request, pk):
    pack = get_object_or_404(Pack, pk=pk)
    unlocked = request.session.get(f"unlocked_{pk}", False)

    return render(request, 'pack_detail.html', {
        'pack': pack,
        'unlocked': unlocked
    })

def unlock_pack(request, pk):
    request.session[f"unlocked_{pk}"] = True
    return redirect('pack_detail', pk=pk)