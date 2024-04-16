from django.db import models
from django.core.exceptions import ValidationError

class FuelType(models.Model):
    type_name = models.CharField(max_length=50)
    price_per_litre = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.type_name

class SubProgram(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Vehicle(models.Model):
    license_plate = models.CharField(max_length=20, unique=True)
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.IntegerField()

    def __str__(self):
        return f"{self.make} {self.model} ({self.license_plate})"

class FuelReceipt(models.Model):
    fuel_type = models.ForeignKey(FuelType, on_delete=models.CASCADE)
    quantity_received = models.DecimalField(max_digits=10, decimal_places=2)  # In litres
    receipt_date = models.DateTimeField(auto_now_add=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.fuel_type.type_name} - {self.quantity_received} litres received"

class FuelAllocation(models.Model):
    sub_program = models.ForeignKey(SubProgram, related_name='fuel_allocations', on_delete=models.CASCADE)
    fuel_receipt = models.ForeignKey(FuelReceipt, related_name='allocations', on_delete=models.CASCADE)
    allocated_litres = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.sub_program.name} - {self.allocated_litres} litres allocated"

class FuelDisbursement(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    fuel_allocation = models.ForeignKey(FuelAllocation, on_delete=models.CASCADE)
    litres = models.DecimalField(max_digits=10, decimal_places=2)  # The amount of fuel disbursed to the vehicle
    disbursement_date = models.DateTimeField(auto_now_add=True)

