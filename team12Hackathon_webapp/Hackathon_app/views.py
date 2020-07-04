from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from Hackathon_app.models import KindMission
import json
# Create your views here.
from Hackathon_app.models import KindAction
from Hackathon_app.submodels.iot_models import BinDevice


def homepage(request):

    return render(request, 'base.html',{})

def dashboard(request):

    return render(request, 'dashboard.html',{})

def missions(request):
        missions = KindMission.objects.all()
        missions = list(missions)
        missions_index = len(missions)
        only_four = missions[:4]
        context = {'missions': list(only_four), 'missions_index': missions_index}
        return render(request, 'missions.html',context=context)



def modal(request):
    return render(request, 'modal.html',{})

def profile(request):
    return render(request, 'profile.html',{})

# this function renders map template with openlayers.
def map_view(request):
    return render(request, 'map.html',{})

def bins_map(request):
    if request.method != 'GET':
        return HttpResponse(status=403)
    bins = BinDevice.objects.all().prefetch_related('Icon')
    res_bins = []
    for b in bins:
        kind_action = KindAction.objects.filter(BinDevice__Id=b.Id)
        bin = {
            'id' : b.Id,
            'longitude' : b.LongitudePosition,
            'latitude' : b.LatitudePosition,
            'b64' : b.Icon.Base64,
            'typeImage' : b.Icon.TypeImage,
            'scale' : b.Icon.Scale,
            'displayName' : b.Icon.DisplayName,
            # 'kindAction' : {
            #     'name' : kind_action.Name,
            #     'description' : kind_action.Description,
            #     'score' : kind_action.Score
            # }
        }
        if kind_action:
            bin['kindAction'] = {
                'name' : kind_action[0].Name,
                'description' : kind_action[0].Description,
                'score' : kind_action[0].Score
            }
        res_bins.append(bin)
    if bins:
        data = {
            'bins' : list(res_bins)
        }
        return JsonResponse(data)
    return HttpResponse(status=204)

def report_map(request):
    if request.method != 'GET':
        return HttpResponse(status=403)
    actions = KindAction.objects.prefetch_related('Report').filter(BinDevice__Id=None)
    if not actions:
        return HttpResponse(status=204)
    res_actions = []
    for a in actions:
        res_actions.append({
            'id' : a.id,
            'name' : a.Name,
            'description' : a.Description,
            'score' : a.Score,
            'startDatetime' : a.StartDateValidation,
            'b64' : a.Report.Icon.Base64,
            'longitude' : a.Report.LongitudePosition,
            'latitude': a.Report.LatitudePosition,
        })
    return JsonResponse({
        'reports' : res_actions
    })
