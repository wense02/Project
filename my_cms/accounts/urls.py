from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('templates/', views.templates, name='templates'),
    path('customer/<str:pk>/', views.customer, name='customer'),
]