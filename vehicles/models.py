from django.db import models
from django.contrib.auth.models import User

class Province(models.Model):
    province_name = models.CharField(max_length=100)

    def __str__(self):
        return self.province_name
    
class Location(models.Model):
    province = models.ForeignKey(Province,   on_delete=models.CASCADE)
    location_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.location_name
    
class Status(models.Model):
    status_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.status_name
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    province = models.ForeignKey(Province, on_delete=models.SET_NULL, null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    
class SubProgramme(models.Model):
    subProgramme_name = models.CharField(max_length=100)
    
class Programme(models.Model):
    subProgramme = models.ForeignKey(SubProgramme, on_delete=models.CASCADE)
    programme_name = models.CharField(max_length = 1000)
    
class Vehicle(models.Model):
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    number_plate = models.CharField(max_length=20, unique=True)
    vehicle_type = models.CharField(max_length=100)
    engine_number = models.CharField(max_length=100)
    classis_number = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.number_plate} - {self.status}"

class Maintenance(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    status_at_service = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True, blank=True, related_name="maintenance_status")
    last_service_mileage = models.IntegerField()
    is_serviced = models.BooleanField(default=False)
    before_next_service_mileage = models.IntegerField()
    next_service_mileage = models.IntegerField()
    next_service_date = models.DateField(null=True)
    service_date = models.DateField(auto_now_add=True, null=True)
    service_type = models.CharField(max_length=500, null=True)
    service_provided= models.CharField(max_length=1000, null=True)
    service_provider= models.CharField(max_length=1000, null=True)
    remarks= models.CharField(max_length=1000, null=True)
    cost_incurred = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Maintenance for {self.vehicle.number_plate}"

class MileageRecord(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='mileage_records')
    mileage_reading = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Mileage record for {self.vehicle.number_plate}"

class FuelDisbursement(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    subProgramme= models.ForeignKey(SubProgramme, on_delete=models.CASCADE,null=True)
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE,null=True)
    driver = models.ForeignKey(UserProfile, on_delete=models.CASCADE,null=True)
    purpose = models.CharField(max_length=1000)
    amount_of_fuel_disbursed = models.DecimalField(max_digits=15, decimal_places=2)
    coupon_serial_number = models.CharField(max_length=50)
    issuer_name = models.CharField(max_length=100)
    transaction_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Fuel disbursement for {self.vehicle.number_plate}"
    