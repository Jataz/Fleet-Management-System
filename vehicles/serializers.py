from rest_framework import serializers
from .models import Location, Province, Status, Vehicle,Maintenance, MileageRecord,FuelDisbursement, VehicleUser


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

class VehicleUserSerializer(serializers.ModelSerializer):
    province_name = serializers.ReadOnlyField(source='province.province_name')
    location_name = serializers.ReadOnlyField(source='location.location_name')
    province_id = serializers.PrimaryKeyRelatedField(queryset=Province.objects.all(), write_only=True, source='province')
    location_id = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all(), write_only=True, source='location')
    
    class Meta:
        model = VehicleUser
        fields = ['id','province_id', 'location_id','province_name', 'location_name','name']
        
    
class VehicleSerializer(serializers.ModelSerializer):
    province_name = serializers.ReadOnlyField(source='province.province_name')
    location_name = serializers.ReadOnlyField(source='location.location_name')
    status_name = serializers.ReadOnlyField(source='status.status_name')
    province_id = serializers.PrimaryKeyRelatedField(queryset=Province.objects.all(), write_only=True, source='province')
    location_id = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all(), write_only=True, source='location')
    status_id = serializers.PrimaryKeyRelatedField(queryset=Status.objects.all(), write_only=True, source='status')

    class Meta:
        model = Vehicle
        fields = ['id', 'province_id', 'location_id', 'status_id', 'number_plate', 'vehicle_type', 'province_name', 'location_name', 'status_name','classis_number','engine_number']
        
class MaintenanceSerializer(serializers.ModelSerializer):
    number_plate = serializers.ReadOnlyField(source='vehicle.number_plate')
    status_name = serializers.ReadOnlyField(source='vehicle.status_name')
    vehicle_id = serializers.PrimaryKeyRelatedField(queryset=Vehicle.objects.all(), write_only=True, source='vehicle')

    class Meta:
        model = Maintenance
        fields = ['id', 'vehicle_id', 'number_plate', 'status_name', 'last_service_mileage', 'before_next_service_mileage', 'next_service_mileage', 'next_service_date', 'service_type', 'cost_incurred']
        extra_kwargs = {
            'before_next_service_mileage': {'read_only': True},
            'next_service_mileage': {'read_only': True},
            'is_serviced': {'read_only': True},  # Assuming this is intended to control record creation
        }

    def create(self, validated_data):
        vehicle = validated_data['vehicle']

        # Check for existing unserviced maintenance records for this vehicle
        unserviced_maintenance_exists = Maintenance.objects.filter(vehicle=vehicle, is_serviced=False).exists()
        if unserviced_maintenance_exists:
            # If there's already an unserviced maintenance record, prevent creating a new one
            raise serializers.ValidationError("This vehicle already has an unserviced maintenance record.")

        last_service_mileage = validated_data.get('last_service_mileage', 0)
        
        validated_data['next_service_mileage'] = last_service_mileage + 10000
        validated_data['before_next_service_mileage'] = 10000

        # Assuming _update_vehicle_status method handles updating vehicle status based on the maintenance record
        self._update_vehicle_status(vehicle, last_service_mileage + 10000)

        # Create the new maintenance record
        new_maintenance_record = super().create(validated_data)

        # Optionally, update the vehicle's status here, if needed

        return new_maintenance_record

    def update(self, instance, validated_data):
        # Assuming last_service_mileage might be updated
        last_service_mileage = validated_data.get('last_service_mileage', instance.last_service_mileage)
        
        instance.next_service_mileage = last_service_mileage + 10000
        instance.before_next_service_mileage = 10000  # This might need to be calculated based on actual current mileage

        # Update other fields as necessary
        # ...

        instance.save()

        # Calculate and update vehicle status
        self._update_vehicle_status(instance.vehicle, last_service_mileage + 10000)

        return instance

    def _update_vehicle_status(self, vehicle, before_next_service_mileage):

        try:
            if before_next_service_mileage <= 10000:  # Placeholder for actual logic
                overdue_status = Status.objects.get(status_name='Serviced')
                vehicle.status = overdue_status
            else:
                # Adjust according to your actual logic
                upcoming_status = Status.objects.get(status_name='Serviced')
                vehicle.status = upcoming_status
            
            vehicle.save()
        except Status.DoesNotExist:
            # Handle the case where the status doesn't exist
            pass

class MaintenanceCloseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maintenance
        fields = ['id', 'service_date', 'service_type', 'service_provided', 'service_provider', 'remarks', 'is_serviced']
        read_only_fields = ['id', 'is_serviced']

    def validate(self, data):
        required_fields = ['service_date', 'service_type', 'service_provided', 'service_provider', 'remarks']
        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        if missing_fields:
            raise serializers.ValidationError({field: "This field is required." for field in missing_fields})
        return data

    def update(self, instance, validated_data):
        instance.is_serviced = True  # Close the maintenance record
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        self._update_vehicle_status(instance.vehicle)
        return instance  
    
    def _update_vehicle_status(self, vehicle):

        try:        
            overdue_status = Status.objects.get(status_name='Serviced')
            vehicle.status = overdue_status 
            vehicle.save()
        except Status.DoesNotExist:
            # Handle the case where the status doesn't exist
            pass    
    
class MileageRecordSerializer(serializers.ModelSerializer):
    number_plate = serializers.ReadOnlyField(source='vehicle.number_plate')
    vehicle_id = serializers.PrimaryKeyRelatedField(queryset=Vehicle.objects.all(), write_only=True, source='vehicle')
    name = serializers.ReadOnlyField(source='vehicle_user.name')
    vehicle_user_id = serializers.PrimaryKeyRelatedField(queryset=VehicleUser.objects.all(), write_only=True, source='vehicle_user')
    province_name = serializers.ReadOnlyField(source='vehicle_user.province.province_name')
    location_name = serializers.ReadOnlyField(source='vehicle_user.location.location_name')
    
    class Meta:
        model = MileageRecord
        fields = ['id', 'vehicle_id', 'number_plate', 'vehicle_user_id', 'name', 'mileage_reading','province_name','location_name','created_at']

    def create(self, validated_data):
        # Create the MileageRecord instance
        mileage_record = MileageRecord.objects.create(**validated_data)
        
        # Immediately update related Maintenance record and vehicle status
        self.update_service_mileage_and_status(mileage_record.vehicle, mileage_record.mileage_reading)
        
        return mileage_record

    def update_service_mileage_and_status(self, vehicle, mileage_reading):
        # Find the related Maintenance record by vehicle
        maintenance = Maintenance.objects.filter(vehicle=vehicle).order_by('-created_at').first()
        if maintenance:
            # Calculate the new before_next_service_mileage
            new_before_next_service_mileage = maintenance.next_service_mileage - mileage_reading
            maintenance.before_next_service_mileage = new_before_next_service_mileage
            
            # Determine the vehicle's status based on the new before_next_service_mileage
            if new_before_next_service_mileage <= 0:
                overdue_status = Status.objects.get(status_name='Overdue')
                vehicle.status = overdue_status
            elif 0 < new_before_next_service_mileage <= 1000:  # Example threshold for 'due'
                due_status = Status.objects.get(status_name='Due')
                vehicle.status = due_status
            else:
                upcoming_status = Status.objects.get(status_name='Serviced')
                vehicle.status = upcoming_status

            # Save the updated Maintenance record and Vehicle status
            maintenance.save()
            vehicle.save()
            
    def validate(self, data):
        """
        Check if the mileage_reading is greater than the last service mileage.
        """
        vehicle = data.get('vehicle')  # 'vehicle' is obtained from the 'source' attribute in 'vehicle_id' field
        
        # Attempt to retrieve the most recent Maintenance record for the vehicle
        last_maintenance = MileageRecord.objects.filter(vehicle=vehicle).order_by('-created_at').first()
        
        
        if last_maintenance:
            # Check if the submitted mileage_reading is greater than the last recorded service mileage
            if data['mileage_reading'] <= last_maintenance.mileage_reading:
                current_mileage = data['mileage_reading']
                message = f"The mileage reading {current_mileage} must be greater than {last_maintenance.mileage_reading}."
                raise serializers.ValidationError(message)
        
        # Return the full collection of validated data if all checks pass
        return data
        
class FuelDisbursementSerializer(serializers.ModelSerializer):
    number_plate = serializers.ReadOnlyField(source='vehicle.number_plate')
    vehicle_id = serializers.PrimaryKeyRelatedField(queryset=Vehicle.objects.all(), write_only=True, source='vehicle')

    class Meta:
        model = FuelDisbursement
        fields = ['id', 'vehicle_id', 'number_plate', 'purpose', 'amount_of_fuel_disbursed', 'coupon_serial_number','driver_name','issuer_name','transaction_date']
