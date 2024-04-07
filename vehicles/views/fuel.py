#for frontend
from datetime import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, render
import requests

#rest framework
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import FuelDisbursementSerializer,SubProgrammeSerializer,ProgrammeSerializer

from ..models import FuelDisbursement, Programme, SubProgramme


class SubProgrammeAPIView(APIView):
    def get(self, request):
        subProgrammes = SubProgramme.objects.all()
        serializer = SubProgrammeSerializer(subProgrammes, many=True)
        return Response({'subProgrammes': serializer.data})

class ProgrammeAPIView(APIView):
    def get(self, request):
        subProgramme_id = request.GET.get('subProgramme_id')
        programmes = Programme.objects.filter(subProgramme_id=subProgramme_id)
        serializer = ProgrammeSerializer(programmes, many=True)
        return Response({'programmes': serializer.data})   
    
#Fuel Disbursement API
class FuelDisbursementList(generics.ListAPIView):
    queryset = FuelDisbursement.objects.all()
    serializer_class = FuelDisbursementSerializer
    
class FuelDisbursementCreate(generics.CreateAPIView):
    queryset = FuelDisbursement.objects.all()
    serializer_class = FuelDisbursementSerializer 

class FuelDisbursementDetail(APIView):
    def get(self, request, pk):
        try:
            fuel_disbursement = FuelDisbursement.objects.get(id=pk)
            serializer = FuelDisbursementSerializer(fuel_disbursement)
            return Response(serializer.data)
        except FuelDisbursement.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class UpdateFuelDisbursement(APIView):
    def get_object(self, pk):
        try:
            return FuelDisbursement.objects.get(id=pk)
        except FuelDisbursement.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, pk):
        fuel_detail_view = FuelDisbursementDetail()
        return fuel_detail_view.get(request, pk)

    def put(self, request, pk):
        fuel_disbursement = self.get_object(pk)
        serializer = FuelDisbursementSerializer(fuel_disbursement, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
  