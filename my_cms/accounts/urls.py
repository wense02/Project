from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('templates/', views.templates, name='templates'),
    path('customer/<str:pk>/', views.customer, name='customer'),
    path('create_website/', views.createWebsite, name='create_website'),
    path('update_website/<str:pk>', views.updateWebsite, name='update_website'),
    path('delete_website/<str:pk>', views.deleteWebsite, name='delete_website'),
    
]