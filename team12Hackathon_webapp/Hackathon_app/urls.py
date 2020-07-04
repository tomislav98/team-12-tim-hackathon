
from django.urls import path
from Hackathon_app import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('map/', views.map_view, name='map'),
    path('missions/', views.missions, name='missions'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('map/bins', views.bins_map, name='bins'),
path('map/reports', views.report_map, name='reports'),
    ]
