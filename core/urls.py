from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [

    # ============================
    # HOME & PACKS
    # ============================
    path('', views.home, name='home'),
    path('packs/', views.pack_list, name='pack_list'),
    path('my-packs/', views.my_packs, name='my_packs'),
    path('pack/<int:pk>/', views.pack_detail, name='pack_detail'),
    path('pack/<int:pk>/unlock/', views.unlock_pack, name='unlock_pack'),


    # ============================
    # AUTH: LOGIN / LOGOUT / REGISTER
    # ============================
    path(
        'login/',
        auth_views.LoginView.as_view(template_name='auth/login.html'),
        name='login'
    ),
    path(
        'logout/',
        auth_views.LogoutView.as_view(next_page='home'),
        name='logout'
    ),
    path('register/', views.register, name='register'),


    # ============================
    # AUTH: CHANGE PASSWORD (LOGGED-IN USERS)
    # ============================
    path(
        'password/change/',
        auth_views.PasswordChangeView.as_view(
            template_name='auth/password_change.html'
        ),
        name='password_change'
    ),
    path(
        'password/change/done/',
        auth_views.PasswordChangeDoneView.as_view(
            template_name='auth/password_change_done.html'
        ),
        name='password_change_done'
    ),


    # ============================
    # AUTH: FORGOT PASSWORD (RESET FLOW)
    # ============================
    path(
        'password/reset/',
        auth_views.PasswordResetView.as_view(
            template_name='auth/password_reset.html'
        ),
        name='password_reset'
    ),
    path(
        'password/reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='auth/password_reset_done.html'
        ),
        name='password_reset_done'
    ),
    path(
        'password/reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='auth/password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),
    path(
        'password/reset/complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='auth/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),


    # ============================
    # PROFILE
    # ============================
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
]
