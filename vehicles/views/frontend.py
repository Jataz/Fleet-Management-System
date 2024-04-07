
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required, permission_required
import requests
from django.conf import settings
#rest framework
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import FuelDisbursement, Location, Maintenance, MileageRecord, Programme, Province, Status, SubProgramme, Vehicle, UserProfile


#Frontend Urls
@login_required(login_url="/login")
def index(request):
 
  return render(request, 'pages/dashboard/index.html')

@login_required(login_url="/login")
def vehicle_list(request):
    # Assuming session-based authentication with your Django backend
    session_id = request.COOKIES.get('sessionid')

    # Make a GET request to fetch a list of vehicles, including the session cookie for authentication
    response = requests.get(
        f'{settings.API_BASE_URL}/api/v1/vehicles-in-my-province/',
        cookies={'sessionid': session_id} if session_id else {}
    )

    if response.status_code == 200:
        vehicles = response.json()  # Extract JSON data from the response
        return render(request, 'pages/vehicle/vehicle.html', {'vehicles': vehicles})
    else:
        # Handle the case where the request was not successful
        return render(request, 'error.html', {'message': 'Failed to fetch vehicles from your province'})
    

@login_required(login_url="/login")
def maintenance_list(request):
    # Assuming session-based authentication with your Django backend
    session_id = request.COOKIES.get('sessionid')

    # Make a GET request to fetch a list of vehicles, including the session cookie for authentication
    response = requests.get(
        f'{settings.API_BASE_URL}/api/v1/maintenance/',
        cookies={'sessionid': session_id} if session_id else {}
    )

    if response.status_code == 200:
        maintenance_list = response.json()  # Extract JSON data from the response
        return render(request, 'pages/maintenance/maintenance.html', {'maintenance_list': maintenance_list})
    else:
        # Handle the case where the request was not successful
        return render(request, 'error.html', {'message': 'Failed to fetch Maintenance list'})

@login_required(login_url="/login")
def mileage_list(request):
    # Assuming session-based authentication with your Django backend
    session_id = request.COOKIES.get('sessionid')

    # Make a GET request to fetch a list of vehicles, including the session cookie for authentication
    response = requests.get(
        f'{settings.API_BASE_URL}/api/v1/mileage/',
        cookies={'sessionid': session_id} if session_id else {}
    )

    if response.status_code == 200:
        mileage_records = response.json()  # Extract JSON data from the response
        return render(request, 'pages/mileage/mileage.html', {'mileage_records': mileage_records})
    else:
        # Handle the case where the request was not successful
        return render(request, 'error.html', {'message': 'Failed to fetch Mileage Vehicles'})

@login_required(login_url="/login")
def fuel_disbursed(request):
    # Make a GET request to fetch a list of vehicles
    response = requests.get(f'{settings.API_BASE_URL}/api/v1/fuel-disbursements/')
    
    # Check if the request was successful
    if response.status_code == 200:
        fuel_disbursements= response.json()  # Extract JSON data from the response
        return render(request, 'pages/fuel/fuel_disbursed.html', {'fuel_disbursements': fuel_disbursements})
    else:
        # Handle the case where the request was not successful
        return render(request, 'error.html', {'message': 'Failed to fetch vehicles'})

@login_required(login_url="/login")  
def fuel_received(request):
    
    response = requests.get(f'{settings.API_BASE_URL}/api/v1/fuel-disbursements/')
    
    if response.status_code == 200:
        fuel_disbursements= response.json()  # Extract JSON data from the response
        return render(request, 'pages/fuel/fuel_received.html', {'fuel_disbursements': fuel_disbursements})
    else:
        # Handle the case where the request was not successful
        return render(request, 'error.html', {'message': 'Failed to fetch vehicles'})
    
  