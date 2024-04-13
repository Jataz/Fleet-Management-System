#rest framework
from django.http import Http404, JsonResponse
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt

from ..models import  FuelType, Location, Maintenance, MileageRecord, Province, Status,Vehicle,UserProfile
from ..serializers import  LocationSerializer,ProvinceSerializer,StatusSerializer,VehicleSerializer,UserProfileSerializer,MaintenanceSerializer,\
    MileageRecordSerializer,FuelTypeSerializer

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db import transaction


#Fuel Type
class FuelTypeAPIView(APIView):
    def get(self, request):
        fueltype = FuelType.objects.all()
        serializer = FuelTypeSerializer(fueltype, many=True)
        return Response({'fueltype': serializer.data})


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
    
""" class UserProfileList(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer    """
    

class UserProfileList(generics.ListAPIView):
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        # Ensure the user is authenticated
        if not self.request.user.is_authenticated:
            raise Http404("User is not authenticated")
        
        # Attempt to get the logged-in user's UserProfile instance
        try:
            user_profile = UserProfile.objects.get(user=self.request.user)
        except UserProfile.DoesNotExist:
            raise Http404("UserProfile for the logged-in user does not exist")
        
        # Filter UserProfiles by the province of the logged-in user
        queryset = UserProfile.objects.filter(province=user_profile.province)
        return queryset

#Vehicle API
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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def vehicles_in_user_province(request):
    # Check if the requesting user is a superuser
    if request.user.is_superuser:
        # Return all vehicles for superusers
        vehicles = Vehicle.objects.all()
        serializer = VehicleSerializer(vehicles, many=True)
        return Response(serializer.data)

    # For regular users, proceed with the original logic
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        return Response({'error': 'UserProfile does not exist for this user.'}, status=status.HTTP_404_NOT_FOUND)

    if user_profile.province:
        vehicles = Vehicle.objects.filter(province=user_profile.province)
        serializer = VehicleSerializer(vehicles, many=True)
        return Response(serializer.data)
    else:
        return Response({'error': 'No province associated with this user.'}, status=status.HTTP_400_BAD_REQUEST)


#The vehicle list for vehicles in province
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def vehicles_lis(request):
    user = request.user
    user_profile_exists = UserProfile.objects.filter(user=user).exists()
    
    # Common logic for fetching vehicles based on province, used for both superusers with a province and regular users
    def get_vehicles_by_province(province):
        vehicles = Vehicle.objects.filter(province=province).exclude(status__status_name="Non Runner")
        serializer = VehicleSerializer(vehicles, many=True)
        return Response(serializer.data)

    # For superusers, check if they have a profile and a province
    if user.is_superuser and user_profile_exists:
        user_profile = UserProfile.objects.get(user=user)
        if user_profile.province:
            return get_vehicles_by_province(user_profile.province)
        else:
            # If the superuser has no associated province, return all vehicles
            vehicles = Vehicle.objects.all()
            serializer = VehicleSerializer(vehicles, many=True)
            return Response(serializer.data)

    # For regular users, use the original logic
    try:
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        return Response({'error': 'UserProfile does not exist for this user.'}, status=status.HTTP_404_NOT_FOUND)

    if user_profile.province:
        return get_vehicles_by_province(user_profile.province)
    else:
        return Response({'error': 'No province associated with this user.'}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def vehicles_list(request):
    user = request.user
    user_profile_exists = UserProfile.objects.filter(user=user).exists()

    # Common logic for fetching vehicles based on province, used for both superusers with a province and regular users
    def get_vehicles_by_province(province):
        # Assuming 'status_name' is a field in your Status model and 'status' is a ForeignKey in your Vehicle model.
        # Adjust 'status_name' comparison value as necessary.
        vehicles = Vehicle.objects.filter(province=province).exclude(status__status_name="Non Runner")
        serializer = VehicleSerializer(vehicles, many=True)
        return Response(serializer.data)

    # For superusers, check if they have a profile and a province
    if user.is_superuser and user_profile_exists:
        user_profile = UserProfile.objects.get(user=user)
        if user_profile.province:
            return get_vehicles_by_province(user_profile.province)
        else:
            # If the superuser has no associated province, return all vehicles excluding non-runners
            vehicles = Vehicle.objects.exclude(status__status_name="Non Runner")
            serializer = VehicleSerializer(vehicles, many=True)
            return Response(serializer.data)

    # For regular users, use the original logic
    try:
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        return Response({'error': 'UserProfile does not exist for this user.'}, status=status.HTTP_404_NOT_FOUND)

    if user_profile.province:
        return get_vehicles_by_province(user_profile.province)
    else:
        return Response({'error': 'No province associated with this user.'}, status=status.HTTP_400_BAD_REQUEST)
    
class VehicleDetailsAPIView(APIView):
    def get(self, request, vehicle_id):
        try:
            # Retrieve the vehicle object
            vehicle = Vehicle.objects.get(pk=vehicle_id)
            
            # Retrieve maintenance records for the vehicle
            maintenance_records = Maintenance.objects.filter(vehicle=vehicle)
            maintenance_serializer = MaintenanceSerializer(maintenance_records, many=True)
            
            # Retrieve mileage records for the vehicle
            mileage_records = MileageRecord.objects.filter(vehicle=vehicle)
            mileage_serializer = MileageRecordSerializer(mileage_records, many=True)
            
            # Combine the data
            data = {
                'vehicle': vehicle.number_plate,
                'maintenance_records': maintenance_serializer.data,
                'mileage_records': mileage_serializer.data
            }
            
            return Response(data, status=status.HTTP_200_OK)
        except Vehicle.DoesNotExist:
            return Response({'error': 'Vehicle not found'}, status=status.HTTP_404_NOT_FOUND)

class VehicleMaintenanceCreate(generics.CreateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        with transaction.atomic():
            vehicle_instance = serializer.save()  # Save the vehicle record
            
            # Create maintenance record
            maintenance_data = {
                'vehicle_id': vehicle_instance.id,  # Assign the vehicle instance
                'last_service_mileage': request.data.get('last_service_mileage'),  # Extract last_service_mileage from request data
                'status_at_service_id': request.data.get('status_at_service_id')
            }
            maintenance_serializer = MaintenanceSerializer(data=maintenance_data)
            maintenance_serializer.is_valid(raise_exception=True)
            maintenance_serializer.save()  # Save the maintenance record
        
        return Response({"message": "Vehicle and Maintenance records created successfully"}, status=status.HTTP_201_CREATED)
