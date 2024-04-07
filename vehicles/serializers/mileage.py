from rest_framework import serializers
from django.contrib.auth.models import User

from ..models import  Location, Province, Status, UserProfile, Vehicle,Maintenance, MileageRecord

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']  # Adjust as needed

class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ['province_name']

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['location_name']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    province = ProvinceSerializer(read_only=True)
    location = LocationSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['user', 'province', 'location']
 
class MileageRecordSerializer(serializers.ModelSerializer):
    number_plate = serializers.ReadOnlyField(source='vehicle.number_plate')
    vehicle_id = serializers.PrimaryKeyRelatedField(queryset=Vehicle.objects.all(), write_only=True, source='vehicle')
    user_profile = UserProfileSerializer(read_only=True)  # Serialize the user who captured the mileage
    province = UserProfileSerializer(read_only=True)
    location = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = MileageRecord
        fields = ['id', 'vehicle_id', 'number_plate', 'user_profile', 'mileage_reading','province','location','created_at']

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
        Check if the mileage_reading is greater than the last service mileage or last recorded mileage.
        """
        vehicle = data.get('vehicle')  # 'vehicle' is obtained from the 'source' attribute in 'vehicle_id' field
        
        # Attempt to retrieve the most recent MileageRecord for the vehicle
        last_mileage_record = MileageRecord.objects.filter(vehicle=vehicle).order_by('-created_at').first()

        # Also attempt to retrieve the most recent Maintenance record for comparison
        last_maintenance_record = Maintenance.objects.filter(vehicle=vehicle).order_by('-created_at').first()

        last_recorded_mileage = 0  # Default to 0 if no records are found

        if last_mileage_record:
            last_recorded_mileage = last_mileage_record.mileage_reading
        elif last_maintenance_record:
            # If there's no MileageRecord but there is a Maintenance record, use its next_service_mileage
            last_recorded_mileage = last_maintenance_record.last_service_mileage

        # Now, compare the submitted mileage_reading with last_recorded_mileage
        if data['mileage_reading'] <= last_recorded_mileage:
            current_mileage = data['mileage_reading']
            message = f"The mileage reading {current_mileage} must be greater than {last_recorded_mileage}."
            raise serializers.ValidationError(message)
        
        # Return the full collection of validated data if all checks pass
        return data

