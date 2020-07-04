from django.shortcuts import render
from django.http import JsonResponse
from Hackathon_app.models import KindMission
import json
# Create your views here.

def homepage(request):

    return render(request, 'base.html',{})

def dashboard(request):

    return render(request, 'dashboard.html',{})

def missions(request):

    return render(request, 'missions.html',{})

def index(request):
    missions = KindMission.objects.all()
    missions = list(missions)
    missions_index = len(missions)
    only_four = missions[:4]
    context = {'missions': list(only_four), 'missions_index': missions_index}
    return render(request, 'index.html',context=context)

def modal(request):
    return render(request, 'modal.html',{})

def profile(request):
    return render(request, 'profile.html',{})

# this function renders map template with openlayers.
def map_view(request):
    print(request.GET)
    if request.method == 'GET' and request.GET: # if get request has data, it's a different call.
        data = {
            'bins' : [
                {
                    'id' : 1,
                    'longitude' : 45.449903,
                    'latitude' : 11.890073
                }
            ]
        }
        print("risposta json")
        return JsonResponse(data)
    return render(request, 'map.html',{})
