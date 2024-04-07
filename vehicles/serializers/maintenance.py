from datetime import datetime
from rest_framework import serializers
from ..models import  Status, Vehicle,Maintenance
from django.db import transaction
from dateutil.relativedelta import relativedelta
from django.utils import timezone


class MaintenanceSerializer(serializers.ModelSerializer):
    number_plate = serializers.ReadOnlyField(source='vehicle.number_plate')
    status_name = serializers.ReadOnlyField(source='status.status_name')
    vehicle_id = serializers.PrimaryKeyRelatedField(queryset=Vehicle.objects.all(), write_only=True, source='vehicle')
    status_at_service_id = serializers.PrimaryKeyRelatedField(queryset=Status.objects.all(), write_only=True, source='status')
    class Meta:
        model = Maintenance
        fields = ['id','status_at_service_id', 'vehicle_id', 'number_plate', 'status_name', 'last_service_mileage', 'before_next_service_mileage', 'next_service_mileage', 'next_service_date', 'service_type', 'cost_incurred','service_date', 'service_type', 'service_provided', 'service_provider', 'remarks', 'is_serviced','updated_at']
        extra_kwargs = {
            'before_next_service_mileage': {'read_only': True},
            'next_service_mileage': {'read_only': True},
            'is_serviced': {'read_only': True},  # Assuming this is intended to control record creation
            'status_name': {'read_only': True},
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
        fields = ['id', 'service_date', 'service_type', 'service_provided', 'service_provider', 'remarks', 'is_serviced','status_at_service']
        read_only_fields = ['id', 'is_serviced', 'status_at_service']

    def validate(self, data):
        
        if self.instance.is_serviced:
            raise serializers.ValidationError("This record has already been serviced")
        return data

    @transaction.atomic
    def update(self, instance, validated_data):
        # Update the current instance to mark it as serviced
        # Use the current date for the service date
        service_date = datetime.now().date()
        
                # Fetch the current vehicle status
        current_status = instance.vehicle.status

        # Set the vehicle's current status on the maintenance record
        instance.status_at_service = current_status

        instance.is_serviced = True
        for key, value in validated_data.items():
            setattr(instance, key, value)
        
        # It's important to actually update the service_date field in your model.
        # Assuming your model has a field named 'service_date' or similar where you store
        # the date of the last service. Adjust the field name as per your model.
        instance.service_date = service_date
        instance.save()

        # Update the vehicle status
        self._update_vehicle_status(instance.vehicle)

        # Create a new maintenance record as a placeholder for the next service
        # Now passing the current date directly
        self._create_next_maintenance_record(instance, service_date)

        return instance


    def _update_vehicle_status(self, vehicle):
        try:
            serviced_status = Status.objects.get(status_name='Serviced')
            vehicle.status = serviced_status
            vehicle.save()
        except Status.DoesNotExist:
            pass  # Optionally, log this error

    def _create_next_maintenance_record(self, previous_instance,service_date):
        # Calculate the next service mileage and before next service mileage
        # This is an example; adjust the logic based on your requirements
        a = previous_instance.next_service_mileage 
        b = previous_instance.before_next_service_mileage
        next_mileage = a - b  # Assuming 'service_mileage' is a field on your model
        

        next_service_date = service_date + relativedelta(months=+6)

        Maintenance.objects.create(
            vehicle=previous_instance.vehicle,
            last_service_mileage=next_mileage,
            next_service_mileage=next_mileage + 10000,  # Placeholder logic
            before_next_service_mileage=10000,  # Placeholder logic
            # Copy other fields from the previous instance or set defaults
            next_service_date=next_service_date,
            service_date=None,  # For DateField, use None to represent a null value
            service_type="",  # For CharField, use an empty string to represent 'no data'
            service_provided="",  # Likewise, use an empty string for CharField
            service_provider="",  # And for any other CharField
            remarks="",  # Example remark; adjust as needed
            is_serviced=False,  # New record is not yet serviced
        )   
