
from django.urls import path
 
from .views import FuelDisbursementCreate, FuelDisbursementDetail, FuelDisbursementList, LocationAPIView, MaintenanceClose,\
    MaintenanceCreate, MileageRecordCreate, MileageRecordDetail, MileageRecordList, ProgrammeAPIView, ProvinceAPIView,\
    StatusAPIView, SubProgrammeAPIView, UpdateFuelDisbursement, UpdateMileageRecord, VehicleCreate,  VehicleDetail,\
    UpdateVehicle,MaintenanceList, MaintenanceDetail, UpdateMaintenance, UserProfileList, MaintenanceApiList,VehicleDetailsAPIView,\
    MileageRecordApiList,  check_vehicle_exists,vehicles_in_user_province,vehicles_list
   
from . import views


urlpatterns = [
    
    path('vehicle-create/', VehicleCreate.as_view(), name='vehicle-create'),
    path('vehicle-detail/<int:pk>/', VehicleDetail.as_view(), name='vehicle-detail'),
    path('update-vehicle/<int:pk>/', UpdateVehicle.as_view(), name='update-vehicle'),
    path('check-number-plate/', check_vehicle_exists, name='check-number-plate'),
    path('vehicles-in-my-province/', vehicles_in_user_province, name='vehicles-in-my-province'),
    path('vehicles/', vehicles_list,name='vehicles'),
    
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
    path('fuel-disbursement-detail/<int:pk>/', FuelDisbursementDetail.as_view(), name='fuel-disbursement-detail'),
    path('fuel-disbursement-update/<int:pk>/', UpdateFuelDisbursement.as_view(), name='fuel-disbursement-update'),
    
    #Dropdowns
    path('provinces/', ProvinceAPIView.as_view(), name='provinces'),
    path('locations/', LocationAPIView.as_view(), name='locations'),
    path('statuses/', StatusAPIView.as_view(), name='status'),
    
    path('vehicle-user-list/', UserProfileList.as_view(), name="vehicle-user-list"), 
    
    path('sub-programmes/', SubProgrammeAPIView.as_view(), name='sub-programmes'),
    path('programmes/', ProgrammeAPIView.as_view(), name='programmes'),
    
    
    #Frontend
    path('dashboard/', views.index ,name='index'),
    path('vehicle-list/', views.vehicle_list, name='vehicle-list'),
    path('maintenance-list/', views.maintenance_list, name='maintenance-list'),
    path('mileage-list/', views.mileage_list, name='mileage-list'),
    path('fuel-disbursed/', views.fuel_disbursed, name='fuel-disbursed'),
    path('fuel-received/',views.fuel_received, name='fuel-received'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.user_logout_view, name='logout'), 
    
    path('vehicle-details/<int:vehicle_id>/', VehicleDetailsAPIView.as_view(), name='vehicle-details-api'),
    path('vehicles/<int:vehicle_id>/maintenance/', MaintenanceApiList.as_view(), name='vehicle-maintenance'),
    path('vehicles/<int:vehicle_id>/mileage/', MileageRecordApiList.as_view(), name='vehicle-mileage')
]
