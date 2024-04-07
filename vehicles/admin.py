from django.contrib import admin
from django.contrib.auth.models import Permission
from .models import FuelDisbursement, Location, Maintenance, MileageRecord, Programme, Province, Status, SubProgramme, UserProfile, Vehicle

class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('id', 'province_name')

class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'province', 'location_name')

class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'status_name')

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'province', 'location')

class SubProgrammeAdmin(admin.ModelAdmin):
    list_display = ('id', 'subProgramme_name')

class ProgrammeAdmin(admin.ModelAdmin):
    list_display = ('id', 'subProgramme', 'programme_name')

class VehicleAdmin(admin.ModelAdmin):
    list_display = ('id', 'province', 'location', 'status', 'number_plate', 'vehicle_type', 'engine_number', 'classis_number', 'created_at', 'updated_at')

class MaintenanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'vehicle', 'last_service_mileage', 'is_serviced', 'before_next_service_mileage', 'next_service_mileage', 'next_service_date', 'service_date', 'service_type'\
        , 'service_provided', 'service_provider', 'remarks', 'cost_incurred','status_at_service','created_at', 'updated_at')

class MileageRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'vehicle', 'user_profile', 'mileage_reading', 'created_at', 'updated_at')

class FuelDisbursementAdmin(admin.ModelAdmin):
    list_display = ('id', 'vehicle', 'subProgramme', 'programme', 'driver', 'purpose', 'amount_of_fuel_disbursed', 'coupon_serial_number', 'issuer_name', 'transaction_date', 'created_at', 'updated_at')

class PermissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'content_type', 'codename')
    
# Register all models with their corresponding admin classes
admin.site.register(Province, ProvinceAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(SubProgramme, SubProgrammeAdmin)
admin.site.register(Programme, ProgrammeAdmin)
admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(Maintenance, MaintenanceAdmin)
admin.site.register(MileageRecord, MileageRecordAdmin)
admin.site.register(FuelDisbursement, FuelDisbursementAdmin)
admin.site.register(Permission, PermissionAdmin)
