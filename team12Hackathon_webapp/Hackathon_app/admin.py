from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django_restful_admin import admin as api_admin
from Hackathon_app.models import User, KindAction, KindMission, BinDevice, KindIconFeature, ReportMap

# Register your models here.
# admin.site.register(User)
admin.site.register(User, UserAdmin)
admin.site.register(KindAction)
admin.site.register(KindMission)
admin.site.register(BinDevice)
admin.site.register(KindIconFeature)
admin.site.register(ReportMap)

api_admin.site.register(KindAction)
api_admin.site.register(BinDevice)
api_admin.site.register(ReportMap)