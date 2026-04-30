from django.shortcuts import render, get_object_or_404
from .models import Pack

def pack_list(request):
    packs = Pack.objects.all().order_by('-created_at')
    return render(request, 'pack_list.html', {'packs': packs})

def pack_detail(request, pk):
    pack = get_object_or_404(Pack, pk=pk)
    return render(request, 'pack_detail.html', {'pack': pack})
