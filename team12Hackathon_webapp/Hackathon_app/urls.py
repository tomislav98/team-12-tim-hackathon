
from django.urls import path
from Hackathon_app import views

urlpatterns = [
    path('', views.homepage, name='home'),
    path('index/', views.index, name='index'),
    path('modal/', views.modal, name='modal'),
    path('map/', views.map_view, name='map'),
    path('profile/', views.profile, name='profile'),
    path('missions/', views.missions, name='missions'),
    path('dashboard/', views.dashboard, name='dashboard'),

    ]
