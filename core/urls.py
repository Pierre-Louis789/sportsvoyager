from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('packs/', views.pack_list, name='pack_list'),
    path('my-packs/', views.my_packs, name='my_packs'),
    # Auth
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='pack_list'), name='logout'),
    path('register/', views.register, name='register'),

    # Packs
    path('pack/<int:pk>/', views.pack_detail, name='pack_detail'),
    path('pack/<int:pk>/unlock/', views.unlock_pack, name='unlock_pack'),
]
