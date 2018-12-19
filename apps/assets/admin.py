from django.contrib import admin


class AssetAdmin(admin.ModelAdmin):
    list_display = ('id', 'sn', 'date',)
    filter_horizontal = ('tag',)


class NewAssetApprovalZoneAdmin(admin.ModelAdmin):
    list_display = ['sn', 'asset_type', 'manufactory', 'model', 'date', 'ram_size', 'cpu_model', 'cpu_core_count']
    list_filter = ['asset_type', 'date']
    search_fields = ('sn',)
    actions=['approve_selected_rows']
    def approve_selected_rows(self):
        pass



# Register your models here.
from apps.assets import models

admin.site.register(models.Asset, AssetAdmin)
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
admin.site.register(models.NewAssetApprovalZone, NewAssetApprovalZoneAdmin)
