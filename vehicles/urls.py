
from django.urls import path
from .views import FuelDisbursementCreate, FuelDisbursementDetail, FuelDisbursementList, LocationAPIView, MaintenanceClose, MaintenanceCreate, MileageRecordAPIView, MileageRecordCreate, MileageRecordDetail, MileageRecordList, ProvinceAPIView, StatusAPIView, UpdateFuelDisbursement, UpdateMileageRecord, VehicleCreate, VehicleList, VehicleDetail, UpdateVehicle,MaintenanceList, MaintenanceDetail, UpdateMaintenance, VehicleUserList, check_vehicle_exists
from . import views


urlpatterns = [
    
    path('vehicles/', VehicleList.as_view()), 
    path('vehicle-create/', VehicleCreate.as_view(), name='vehicle-create'),
    path('vehicle-detail/<int:pk>/', VehicleDetail.as_view(), name='vehicle-detail'),
    path('update-vehicle/<int:pk>/', UpdateVehicle.as_view(), name='update-vehicle'),
    path('check-number-plate/', check_vehicle_exists, name='check-number-plate'),
    
    #Maintenance API
    path('maintenance/', MaintenanceList.as_view(), name='maintenance'),
    path('maintenance-create/', MaintenanceCreate.as_view(), name='maintenance-create'),
    path('maintenance-detail/<int:pk>/', MaintenanceDetail.as_view(), name='maintenance-detail'),
    path('maintenance-update/<int:pk>/', UpdateMaintenance.as_view(), name='maintenance-update'),
    path('maintenance-close/<int:pk>/', MaintenanceClose.as_view(), name='maintenance-close'),  
    
    #Mileage API
    path('mileage/', MileageRecordList.as_view(), name='mileage'),
    path('mileage-create/', MileageRecordCreate.as_view(), name='mileage-create'),
    path('mileage-detail/<int:pk>/', MileageRecordDetail.as_view(), name='mileage-detail'),
    path('mileage-update/<int:pk>/', UpdateMileageRecord.as_view(), name='mileage-update'),
    
    #Fuel Disbursememt API
    path('fuel-disbursements/', FuelDisbursementList.as_view(), name='fuel-disbursement'),
     path('fuel-disbursement-create/', FuelDisbursementCreate.as_view(), name='fuel-disbursement-create'),
    path('fuel-disbursement-deatil/<int:pk>/', FuelDisbursementDetail.as_view(), name='fuel-disbursement-detail'),
    path('fuel-disbursement-update/<int:pk>/', UpdateFuelDisbursement.as_view(), name='fuel-disbursement-update'),
    
    #Dropdowns
    path('provinces/', ProvinceAPIView.as_view(), name='provinces'),
    path('locations/', LocationAPIView.as_view(), name='locations'),
    path('statuses/', StatusAPIView.as_view(), name='status'),
    path('vehicle-user-list/', VehicleUserList.as_view(), name="vehicle-user-list"), 
    
    path('province/<int:province_id>/', views.ProvinceDetailView.as_view(), name='province_detail'),
    path('location/<int:location_id>/', views.LocationDetailView.as_view(), name='location_detail'),
    path('status/<int:status_id>/', views.StatusDetailView.as_view(), name='status_detail'),
    
    #Frontend
    path('', views.index ,name='index'),
    path('vehicle-list/', views.vehicle_list, name='vehicle-list'),
    path('maintenance-list/', views.maintenance_list, name='maintenance-list'),
    path('mileage-list/', views.mileage_list, name='mileage-list'),
    path('fuel-list/', views.fuel_list, name='fuel-list'),
    
    
    path('mileage_record/', MileageRecordAPIView.as_view(), name='api_mileage_record'),

]
