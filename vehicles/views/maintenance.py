#rest framework
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import MaintenanceSerializer,MaintenanceCloseSerializer

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from ..models import Maintenance, UserProfile, Vehicle


class MaintenanceList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user

        # Check if the user is a superuser
        if user.is_superuser:
            # Return all maintenance records for superusers
            all_maintenance_records = Maintenance.objects.all().order_by('-created_at')
            serializer = MaintenanceSerializer(all_maintenance_records, many=True)
            return Response(serializer.data)

        # For regular users, check for UserProfile and province
        try:
            user_profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            return Response({'error': 'UserProfile does not exist for this user.'}, status=404)

        if not user_profile.province:
            return Response({'error': 'No province associated with this user.'}, status=400)

        # Filtering Maintenance records by the user's province
        maintenance_records = Maintenance.objects.filter(vehicle__province=user_profile.province).order_by('-created_at')
        serializer = MaintenanceSerializer(maintenance_records, many=True)
        return Response(serializer.data)
    
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
    
""" class MaintenanceClose(APIView):
    def patch(self, request, pk):
        maintenance = Maintenance.objects.get(pk=pk)
        serializer = MaintenanceCloseSerializer(maintenance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) """

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
        
        # Create a mutable copy of the request.data
        data = request.data.copy()
        # Modify the mutable copy
        data['is_serviced'] = True

        serializer = MaintenanceCloseSerializer(maintenance, data=data, partial=True)  # Allow partial update
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MaintenanceApiList(APIView):
    """
    List all maintenance records for a vehicle that are serviced.
    """
    def get(self, request, vehicle_id):
        # Filter maintenance records by vehicle_id and is_serviced=True
        maintenance = Maintenance.objects.filter(vehicle_id=vehicle_id, is_serviced=True).order_by('-service_date')
        serializer = MaintenanceSerializer(maintenance, many=True)
        return Response(serializer.data)