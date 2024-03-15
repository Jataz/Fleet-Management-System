from django.contrib import admin
from .models import FuelDisbursement, Location, Maintenance, MileageRecord, Province, Status, Vehicle, VehicleUser

admin.site.register(Vehicle)
admin.site.register(Maintenance)
admin.site.register(MileageRecord)
admin.site.register(FuelDisbursement)
admin.site.register(Province)
admin.site.register(Location)
admin.site.register(Status)
admin.site.register(VehicleUser)



# Register your models here.
