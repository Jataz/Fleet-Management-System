from rest_framework import serializers
from ..models import Programme, SubProgramme, Vehicle,FuelDisbursement, UserProfile,FuelReceipt,FuelType,FuelAllocation

  
class SubProgrammeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubProgramme
        fields = ['id','subProgramme_name']
        
class ProgrammeSerializer(serializers.ModelSerializer):
    class Meta:
        model= Programme
        fields = ['id','programme_name']
        
class FuelReceivedSerializer(serializers.ModelSerializer):
    fuel_type = serializers.ReadOnlyField(source='fueltype.fuel_type_name')
    fueltype_id = serializers.PrimaryKeyRelatedField(queryset=FuelType.objects.all(), write_only=True, source='fueltype')
    
    class Meta:
        model = FuelReceipt
        fields = ['id', 'fueltype_id', 'fuel_type', 'quantity_received', 'received_date','monthly','cost','is_used']

class FuelAllocationSerializer(serializers.ModelSerializer):
    subProgramme_name = serializers.ReadOnlyField(source='subProgramme.subProgramme_name')
    subProgramme_id = serializers.PrimaryKeyRelatedField(queryset=SubProgramme.objects.all(), write_only=True, source='subProgramme')
    fuel_type = serializers.ReadOnlyField(source='fueltype.fuel_type_name')
    fueltype_id = serializers.PrimaryKeyRelatedField(queryset=FuelType.objects.all(), write_only=True, source='fueltype')
    class Meta:
        model = FuelAllocation
        fields = ['id', 'fueltype_id', 'fuel_type', 'quantity_received', 'received_date', 'cost']

class FuelDisbursementSerializer(serializers.ModelSerializer):
    number_plate = serializers.ReadOnlyField(source='vehicle.number_plate')
    subProgramme_name = serializers.ReadOnlyField(source='subProgramme.subProgramme_name')
    programme_name = serializers.ReadOnlyField(source='programme.programme_name')
    driver_name = serializers.ReadOnlyField(source='driver.name')
    vehicle_id = serializers.PrimaryKeyRelatedField(queryset=Vehicle.objects.all(), write_only=True, source='vehicle')
    subProgramme_id = serializers.PrimaryKeyRelatedField(queryset=SubProgramme.objects.all(), write_only=True, source='subProgramme')
    programme_id = serializers.PrimaryKeyRelatedField(queryset=Programme.objects.all(), write_only=True, source='programme')
    driver_id = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all(), write_only=True, source='driver')

    class Meta:
        model = FuelDisbursement
        fields = ['id', 'vehicle_id','driver_id','driver_name','subProgramme_id','programme_id', 'number_plate','subProgramme_name','programme_name', 'purpose', 'amount_of_fuel_disbursed', 'coupon_serial_number','driver_name','issuer_name','transaction_date']
