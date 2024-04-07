#for frontend
from datetime import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required, permission_required
from rest_framework import status,permissions
import requests

#rest framework
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from ..models import  MileageRecord, UserProfile
from ..serializers import  MileageRecordSerializer

#Mileage API
""" class MileageRecordList(generics.ListAPIView):
    
    serializer_class = MileageRecordSerializer
    
    def get_queryset(self):
        # Get the queryset of Maintenance objects ordered by the created_at field in descending order
        queryset = MileageRecord.objects.order_by('-created_at')
        return queryset
     """

class MileageRecordList(generics.ListAPIView):
    serializer_class = MileageRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # Check if the user is a superuser and has a UserProfile
        if user.is_superuser:
            try:
                user_profile = UserProfile.objects.get(user=user)
                # For superusers with a province, return all MileageRecord instances in their province
                if user_profile.province:
                    return MileageRecord.objects.filter(vehicle__province=user_profile.province).order_by('-created_at')
                # If the superuser has no associated province, return all records
                return MileageRecord.objects.all().order_by('-created_at')
            except UserProfile.DoesNotExist:
                # If the superuser does not have a UserProfile, return all records
                return MileageRecord.objects.all().order_by('-created_at')

        # For regular users, filter MileageRecord instances based on the user's profile
        try:
            user_profile = UserProfile.objects.get(user=user)
            return MileageRecord.objects.filter(user_profile=user_profile).order_by('-created_at')
        except UserProfile.DoesNotExist:
            # If the regular user does not have a profile, return an empty queryset
            return MileageRecord.objects.none()
    
class MileageRecordCreate(APIView):
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        serializer = MileageRecordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user_profile, created = UserProfile.objects.get_or_create(user=self.request.user)
            serializer.save(user_profile=user_profile)
            #serializer.save()
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
    
    
class MileageRecordApiList(APIView):
    """
    List all mileage records for a vehicle.
    """
    def get(self, request, vehicle_id):
        mileage_records = MileageRecord.objects.filter(vehicle_id=vehicle_id).order_by('-created_at')
        serializer = MileageRecordSerializer(mileage_records, many=True)
        return Response(serializer.data)