from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('create_message/', views.create_message, name='create_message')
]
