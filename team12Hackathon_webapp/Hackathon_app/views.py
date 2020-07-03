from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json
# Create your views here.
from Hackathon_app.submodels.iot_models import BinDevice


def homepage(request):

    return render(request, 'base.html',{})

def index(request):
    return render(request, 'index.html',{})

def modal(request):
    return render(request, 'modal.html',{})

# this function renders map template with openlayers.
def map_view(request):
    print(request.GET)
    if request.method == 'GET' and request.GET: # if get request has data, it's a different call.
        bins = BinDevice.objects.all().prefetch_related('Icon')
        res_bins = []
        for b in bins:
            res_bins.append({
                'id' : b.Id,
                'longitude' : b.LongitudePosition,
                'latitude' : b.LatitudePosition,
                'b64' : b.Icon.Base64,
                'typeImage' : b.Icon.TypeImage
            })
        if bins:
            data = {
                'bins' : list(res_bins)
            }
            return JsonResponse(data)
        return HttpResponse(status=204)
    return render(request, 'map.html',{})
