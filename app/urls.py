from django.urls import path
from django.contrib.auth import views as view
from . import views


urlpatterns = [
    path('', views.main, name='main'),
    path('create_message/', views.create_message, name='create_message'),
    path('login/', view.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
]