from django.urls import path
from . import views

urlpatterns = [
    path('', views.pack_list, name='pack_list'),
    path('pack/<int:pk>/', views.pack_detail, name='pack_detail'),
]
