from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/random-restaurant/', views.get_random_restaurant, name='random_restaurant'),
] 