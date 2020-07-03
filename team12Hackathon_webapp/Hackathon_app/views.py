from django.shortcuts import render
from django.http import JsonResponse
import json
# Create your views here.

def homepage(request):

    return render(request, 'base.html',{})

def index(request):
    return render(request, 'index.html',{})

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