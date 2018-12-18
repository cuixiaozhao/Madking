from django.contrib import admin

# Register your models here.
from apps.assets import models

admin.site.register(models.Asset)
admin.site.register(models.BusinessUnit)
admin.site.register(models.IDC)
admin.site.register(models.Server)
admin.site.register(models.NetworkDevice)
admin.site.register(models.SecurityDevice)
admin.site.register(models.NIC)
admin.site.register(models.CPU)
admin.site.register(models.Ram)
admin.site.register(models.Disk)
admin.site.register(models.RaidAdaptor)
admin.site.register(models.Contract)
admin.site.register(models.UserProfile)
admin.site.register(models.EventLog)
admin.site.register(models.Tag)
