from django.shortcuts import render, get_object_or_404, redirect
from django.db import models
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from packs.models import Pack, UnlockedPack, Comment
from packs.forms import PackForm
from core.forms import CommentForm


import stripe
from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse


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

    unlocked = False
    if request.user.is_authenticated:
        unlocked = UnlockedPack.objects.filter(user=request.user, pack=pack).exists()

    return render(request, 'packs/pack_detail.html', {
        'pack': pack,
        'comments': comments,
        'form': form,
        'unlocked': unlocked,
    })


@login_required
def unlock_pack(request, pk):
    pack = get_object_or_404(Pack, pk=pk)
    UnlockedPack.objects.get_or_create(user=request.user, pack=pack)
    return redirect('pack_detail', pk=pk)


@login_required
def my_packs(request):
    unlocked = UnlockedPack.objects.filter(user=request.user).select_related('pack')
    return render(request, 'packs/my_packs.html', {'unlocked': unlocked})


@login_required
def comment(request, pk):
    pack = get_object_or_404(Pack, pk=pk)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.pack = pack
            comment.user = request.user
            comment.save()
            return redirect('pack_detail', pk=pk)
    else:
        form = CommentForm()

    return render(request, 'packs/comment_form.html', {'form': form, 'pack': pack})


@login_required
def comment_edit(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if request.user != comment.user:
        return redirect('pack_detail', pk=comment.pack.pk)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('pack_detail', pk=comment.pack.pk)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'packs/comment_edit.html', {'form': form, 'comment': comment})


@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if request.user != comment.user:
        return redirect('pack_detail', pk=comment.pack.pk)

    if request.method == "POST":
        comment.delete()
        return redirect('pack_detail', pk=comment.pack.pk)

    return render(request, 'packs/comment_delete.html', {'comment': comment})


@login_required
def checkout(request, pk):
    pack = get_object_or_404(Pack, pk=pk)

    if UnlockedPack.objects.filter(user=request.user, pack=pack).exists():
        return redirect('pack_detail', pk=pk)

    return render(request, 'payment/checkout.html', {
        'pack': pack,
        'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY
    })


@login_required
def payment_success(request, pk):
    pack = get_object_or_404(Pack, pk=pk)

    UnlockedPack.objects.get_or_create(user=request.user, pack=pack)

    request.user.email_user(
        subject=f"Your purchase: {pack.title}",
        message=(
            f"Hi {request.user.username},\n\n"
            f"You have successfully unlocked the pack: {pack.title}.\n"
            "Enjoy your trip planning!\n\n"
            "Sports Voyager"
        )
    )

    return render(request, 'payment/success.html', {'pack': pack})


@staff_member_required
def pack_create(request):
    if request.method == "POST":
        form = PackForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('pack_list')
    else:
        form = PackForm()

    return render(request, 'packs/pack_forms.html', {'form': form, 'mode': 'Create'})


@staff_member_required
def pack_edit(request, pk):
    pack = get_object_or_404(Pack, pk=pk)

    if request.method == "POST":
        form = PackForm(request.POST, request.FILES, instance=pack)
        if form.is_valid():
            form.save()
            return redirect('pack_detail', pk=pk)
    else:
        form = PackForm(instance=pack)

    return render(request, 'packs/pack_forms.html', {'form': form, 'mode': 'Edit'})


@staff_member_required
def pack_delete(request, pk):
    pack = get_object_or_404(Pack, pk=pk)

    if request.method == "POST":
        pack.delete()
        return redirect('pack_list')

    return render(request, 'packs/pack_delete.html', {'pack': pack})


@login_required
def create_checkout_session(request, pk):
    pack = get_object_or_404(Pack, pk=pk)

    stripe.api_key = settings.STRIPE_SECRET_KEY

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        mode='payment',
        line_items=[{
            'price_data': {
                'currency': 'gbp',
                'product_data': {
                    'name': pack.title,
                },
                'unit_amount': int(pack.price * 100),
            },
            'quantity': 1,
        }],
        success_url=request.build_absolute_uri(
            reverse('payment_success', args=[pack.pk])
        ),
        cancel_url=request.build_absolute_uri(
            reverse('pack_detail', args=[pack.pk])
        ),
    )

    return JsonResponse({'id': session.id})
