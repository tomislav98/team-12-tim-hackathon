from django.contrib import admin
from Hackathon_app.models import User, KindAction, KindMission, BinDevice, KindIconFeature

# Register your models here.
admin.site.register(User)
admin.site.register(KindAction)
admin.site.register(KindMission)
admin.site.register(BinDevice)
admin.site.register(KindIconFeature)