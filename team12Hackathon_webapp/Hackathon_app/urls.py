
from django.urls import path
from Hackathon_app import views

urlpatterns = [
    path('', views.homepage, name='home'),
    path('index/', views.index, name='index'),
    path('map/', views.map_view, name='map'),

    ]
