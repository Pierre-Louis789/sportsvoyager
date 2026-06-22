from django.urls import path
from . import views

urlpatterns = [
    path('', views.pack_list, name='pack_list'),
    path('my-packs/', views.my_packs, name='my_packs'),
    #Premium
    path('pack/<int:pk>/', views.pack_detail, name='pack_detail'),
    path('pack/<int:pk>/unlock/', views.unlock_pack, name='unlock_pack'),
    path('pack/<int:pk>/checkout/', views.checkout, name='checkout'),
    path('pack/<int:pk>/payment-success/', views.payment_success, name='payment_success'),

    # Admin
    path('add/', views.pack_create, name='pack_create'),
    path('pack/<int:pk>/edit/', views.pack_edit, name='pack_edit'),
    path('pack/<int:pk>/delete/', views.pack_delete, name='pack_delete'),
]
