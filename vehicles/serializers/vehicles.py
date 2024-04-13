from datetime import datetime
from rest_framework import serializers
from ..models import FuelType, Location, Programme, Province, Status, SubProgramme, Vehicle,Maintenance, MileageRecord,FuelDisbursement, UserProfile
from django.db import transaction
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django.contrib.auth.models import User

class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ['id', 'province_name']

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'location_name']

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['id', 'status_name']
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name'] 

class FuelTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FuelType
        fields = ['id', 'fuel_type_name']
        
class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    province_name = serializers.ReadOnlyField(source='province.province_name')
    location_name = serializers.ReadOnlyField(source='location.location_name')
    province_id = serializers.PrimaryKeyRelatedField(queryset=Province.objects.all(), write_only=True, source='province')
    location_id = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all(), write_only=True, source='location')
    
    class Meta:
        model = UserProfile
        fields = ['id','user','first_name','last_name','province_id', 'location_id','province_name', 'location_name']
        
    
class VehicleSerializer(serializers.ModelSerializer):
    province_name = serializers.ReadOnlyField(source='province.province_name')
    location_name = serializers.ReadOnlyField(source='location.location_name')
    status_name = serializers.ReadOnlyField(source='status.status_name')
    fuel_type = serializers.ReadOnlyField(source='fueltype.fuel_type_name')
    province_id = serializers.PrimaryKeyRelatedField(queryset=Province.objects.all(), write_only=True, source='province')
    location_id = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all(), write_only=True, source='location')
    status_id = serializers.PrimaryKeyRelatedField(queryset=Status.objects.all(), write_only=True, source='status')
    fueltype_id = serializers.PrimaryKeyRelatedField(queryset=FuelType.objects.all(), write_only=True, source='fueltype')

    class Meta:
        model = Vehicle
        fields = ['id', 'province_id','fueltype_id', 'location_id','fuel_type', 'status_id', 'number_plate', 'vehicle_type',\
            'province_name', 'location_name', 'status_name','classis_number','engine_number']
        
