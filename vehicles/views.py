#for frontend
from datetime import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import requests

#rest framework
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import FuelDisbursement, Location, Maintenance, MileageRecord, Province, Status, Vehicle, VehicleUser
from .serializers import FuelDisbursementSerializer, LocationSerializer, MaintenanceCloseSerializer, MaintenanceSerializer, MileageRecordSerializer, ProvinceSerializer, StatusSerializer, VehicleSerializer, VehicleUserSerializer


#Cascading Dropdown
class ProvinceAPIView(APIView):
    def get(self, request):
        provinces = Province.objects.all()
        serializer = ProvinceSerializer(provinces, many=True)
        return Response({'provinces': serializer.data})

class LocationAPIView(APIView):
    def get(self, request):
        province_id = request.GET.get('province_id')
        locations = Location.objects.filter(province_id=province_id)
        serializer = LocationSerializer(locations, many=True)
        return Response({'locations': serializer.data})
    
class StatusAPIView(APIView):
    def get(self, request):
        status = Status.objects.all()
        serializer = StatusSerializer(status, many=True)
        return Response({'status': serializer.data})
    

class ProvinceDetailView(APIView):
    def get(self, request, province_id):
        province = Province.objects.get(pk=province_id)
        data = {'province_name': province.province_name}  # Assuming 'province_name' is the field to be returned
        return Response(data)

class LocationDetailView(APIView):
    def get(self, request, location_id):
        location = Location.objects.get(pk=location_id)
        data = {'location_name': location.location_name}  # Assuming 'location_name' is the field to be returned
        return Response(data)

class StatusDetailView(APIView):
    def get(self, request, status_id):
        status = Status.objects.get(pk=status_id)
        data = {'status_name': status.status_name}  # Assuming 'status_name' is the field to be returned
        return Response(data)

class VehicleUserList(generics.ListAPIView):
    queryset = VehicleUser.objects.all()
    serializer_class = VehicleUserSerializer   

#Vehicle API
class VehicleList(generics.ListAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    
class VehicleCreate(generics.CreateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    
class VehicleDetail(APIView):
    def get(self, request, pk):
        try:
            vehicle = Vehicle.objects.get(id=pk)
            serializer = VehicleSerializer(vehicle)
            return Response(serializer.data)
        except Vehicle.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
class UpdateVehicle(APIView):
    def get_object(self, pk):
        try:
            return Vehicle.objects.get(id=pk)
        except Vehicle.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, pk):
        return VehicleDetail.get(self, request, pk)  # Reuse logic from VehicleDetail

    def put(self, request, pk):
        vehicle = self.get_object(pk)
        serializer = VehicleSerializer(vehicle, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def check_vehicle_exists(request):
    if request.method == 'POST':
        number_plate = request.POST.get('number_plate', None)
        if number_plate:
            # Check if a vehicle with the given number plate exists
            vehicle_exists = Vehicle.objects.filter(number_plate=number_plate).exists()
            return JsonResponse({'exists': vehicle_exists})
    return JsonResponse({'error': 'Invalid request'}, status=400)
        
#Maintenance API
class MaintenanceList(generics.ListAPIView):
    queryset = Maintenance.objects.all()
    serializer_class = MaintenanceSerializer

""" class MaintenanceCreate(generics.CreateAPIView):
    queryset = Maintenance.objects.all()
    serializer_class = MaintenanceSerializer   """ 
    
class MaintenanceCreate(APIView):
    def post(self, request, *args, **kwargs):
        serializer = MaintenanceSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message": "Maintenance record created successfully"}, status=status.HTTP_201_CREATED)
        # With raise_exception=True, you don't need the below line, but it's here for clarity.
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   
    
    def handle_exception(self, exc):
        # Check if the exception is a ValidationError with non_field_errors
        if hasattr(exc, 'get_full_details'):
            error_detail = exc.get_full_details()
            if 'non_field_errors' in error_detail:
                # Extract the non-field error message
                custom_error_message = error_detail['non_field_errors'][0]['message']
                # Return a custom response format
                return Response({"Error": custom_error_message}, status=status.HTTP_400_BAD_REQUEST)

        # Fallback to the default exception handling for other types of exceptions
        return super().handle_exception(exc)
     
class MaintenanceDetail(APIView):
    def get(self, request, pk):
        try:
            maintenance = Maintenance.objects.get(id=pk)
            serializer = MaintenanceSerializer(maintenance)
            return Response(serializer.data)
        except Maintenance.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
class UpdateMaintenance(APIView):
    def get_object(self, pk):
        try:
            return Maintenance.objects.get(id=pk)
        except Maintenance.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, pk):
        return MaintenanceDetail.get(self, request, pk)  # Reuse logic from MaintenanceDetail

    def put(self, request, pk):
        maintenance = self.get_object(pk)
        serializer = MaintenanceSerializer(maintenance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class MaintenanceClose(APIView):
    def patch(self, request, pk):
        maintenance = Maintenance.objects.get(pk=pk)
        serializer = MaintenanceCloseSerializer(maintenance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MaintenanceClose(APIView):
    def get_object(self, pk):
        try:
            return Maintenance.objects.get(pk=pk)
        except Maintenance.DoesNotExist:
            return Response({'message': 'Maintenance record not found.'}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        maintenance = self.get_object(pk)
        if isinstance(maintenance, Response):  # Check if get_object returned a 404 Response
            return maintenance
        serializer = MaintenanceCloseSerializer(maintenance)
        return Response(serializer.data)

    def put(self, request, pk):
        maintenance = self.get_object(pk)
        if isinstance(maintenance, Response):  # Check if get_object returned a 404 Response
            return maintenance

        # Set is_serviced=True directly before passing to serializer for validation and saving
        request.data['is_serviced'] = True

        serializer = MaintenanceCloseSerializer(maintenance, data=request.data, partial=True)  # Allow partial update
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Mileage API
class MileageRecordList(generics.ListAPIView):
    queryset = MileageRecord.objects.all()
    serializer_class = MileageRecordSerializer
    
""" class MileageRecordCreate(generics.CreateAPIView):
    queryset = MileageRecord.objects.all()
    serializer_class = MileageRecordSerializer  """

class MileageRecordCreate(APIView):
    def post(self, request, *args, **kwargs):
        serializer = MileageRecordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message": "Maintenance record created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def handle_exception(self, exc):
        # Check if the exception is a ValidationError with non_field_errors
        if hasattr(exc, 'get_full_details'):
            error_detail = exc.get_full_details()
            if 'non_field_errors' in error_detail:
                # Extract the non-field error message
                custom_error_message = error_detail['non_field_errors'][0]['message']
                # Return a custom response format
                return Response({"Error": custom_error_message}, status=status.HTTP_400_BAD_REQUEST)

        # Fallback to the default exception handling for other types of exceptions
        return super().handle_exception(exc)

class MileageRecordDetail(APIView):
    def get(self, request, pk):
        try:
            mileage_record = MileageRecord.objects.get(id=pk)
            serializer = MileageRecordSerializer(mileage_record)
            return Response(serializer.data)
        except MileageRecord.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class UpdateMileageRecord(APIView):
    def get_object(self, pk):
        try:
            return MileageRecord.objects.get(id=pk)
        except MileageRecord.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, pk):
        mileage_detail_view = MileageRecordDetail()
        return mileage_detail_view.get(request, pk)

    def put(self, request, pk):
        mileage_record = self.get_object(pk)
        serializer = MileageRecordSerializer(mileage_record, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#Fuel Disbursement API
class FuelDisbursementList(generics.ListAPIView):
    queryset = FuelDisbursement.objects.all()
    serializer_class = FuelDisbursementSerializer
    
class FuelDisbursementCreate(generics.CreateAPIView):
    queryset = FuelDisbursement.objects.all()
    serializer_class = FuelDisbursementSerializer 

class FuelDisbursementDetail(APIView):
    def get(self, request, pk):
        try:
            fuel_disbursement = FuelDisbursement.objects.get(id=pk)
            serializer = FuelDisbursementSerializer(fuel_disbursement)
            return Response(serializer.data)
        except FuelDisbursement.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class UpdateFuelDisbursement(APIView):
    def get_object(self, pk):
        try:
            return FuelDisbursement.objects.get(id=pk)
        except FuelDisbursement.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, pk):
        fuel_detail_view = FuelDisbursementDetail()
        return fuel_detail_view.get(request, pk)

    def put(self, request, pk):
        fuel_disbursement = self.get_object(pk)
        serializer = FuelDisbursementSerializer(fuel_disbursement, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    #Frontend Urls

def index(request):
 
  return render(request, 'pages/dashboard/index.html')

def vehicle_list(request):
    # Make a GET request to fetch a list of vehicles
    response = requests.get('http://127.0.0.1:8000/api/v1/vehicles/')
    
    # Check if the request was successful
    if response.status_code == 200:
        vehicles = response.json()  # Extract JSON data from the response
        return render(request, 'pages/vehicle/vehicle.html', {'vehicles': vehicles})
    else:
        # Handle the case where the request was not successful
        return render(request, 'error.html', {'message': 'Failed to fetch vehicles'})
    
def maintenance_list(request):
    # Make a GET request to fetch a list of vehicles
    response = requests.get('http://127.0.0.1:8000/api/v1/maintenance')
    
    # Check if the request was successful
    if response.status_code == 200:
        maintenance_list = response.json()  # Extract JSON data from the response
        return render(request, 'pages/maintenance/maintenance.html', {'maintenance_list': maintenance_list})
    else:
        # Handle the case where the request was not successful
        return render(request, 'error.html', {'message': 'Failed to fetch Maintenance list'})

def mileage_list(request):
    # Make a GET request to fetch a list of vehicles
    response = requests.get('http://127.0.0.1:8000/api/v1/mileage/')
    
    # Check if the request was successful
    if response.status_code == 200:
        mileage_records = response.json()  # Extract JSON data from the response
        return render(request, 'pages/mileage/mileage.html', {'mileage_records': mileage_records})
    else:
        # Handle the case where the request was not successful
        return render(request, 'error.html', {'message': 'Failed to fetch vehicles'})

def fuel_list(request):
    # Make a GET request to fetch a list of vehicles
    response = requests.get('http://127.0.0.1:8000/api/v1/fuel-disbursements/')
    
    # Check if the request was successful
    if response.status_code == 200:
        fuel_disbursements= response.json()  # Extract JSON data from the response
        return render(request, 'pages/fuel/fuel.html', {'fuel_disbursements': fuel_disbursements})
    else:
        # Handle the case where the request was not successful
        return render(request, 'error.html', {'message': 'Failed to fetch vehicles'})






class MileageRecordAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = MileageRecordSerializer(data=request.data)
        if serializer.is_valid():
            mileage_record = serializer.save()
            self.update_service_mileage(mileage_record.vehicle_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update_service_mileage(self, vehicle_id):
        # Similar logic as provided in your function
        latest_mileage_record = MileageRecord.objects.filter(vehicle_id=vehicle_id).order_by('-created_at').first()
        
        if latest_mileage_record:
            mileage_reading = latest_mileage_record.mileage_reading
            maintenance = Maintenance.objects.filter(vehicle_id=vehicle_id).order_by('-created_at').first()

            if maintenance:
                before_next_service_mileage = max(maintenance.next_service_mileage - mileage_reading, 0)
                maintenance.before_next_service_mileage = before_next_service_mileage
                maintenance.save()