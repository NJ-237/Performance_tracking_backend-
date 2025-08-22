from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.contrib.auth import login
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from .models import Shift, BroyeurData, SecheurData, PortData, ExpeditionData
from .serializers import ShiftSerializer, BroyeurDataSerializer, SecheurDataSerializer, PortDataSerializer, ExpeditionDataSerializer
from rest_framework import viewsets


@api_view(['POST'])
def register_user(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_user(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data
        login(request, user)
        return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
    if not serializer.is_valid():
        print(serializer.errors)
        # return Response(serializer.errors, status=400)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

   

# Create your views here.

# views.py for the input values from the ReportSide 

class ShiftViewSet(viewsets.ModelViewSet):
    queryset = Shift.objects.all()
    serializer_class = ShiftSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['get'])
    def broyeur_data(self, request, pk=None):
        shift = self.get_object()
        broyeur_data = shift.broyeur_data.all()
        serializer = BroyeurDataSerializer(broyeur_data, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def secheur_data(self, request, pk=None):
        shift = self.get_object()
        secheur_data = shift.secheur_data.all()
        serializer = SecheurDataSerializer(secheur_data, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def port_data(self, request, pk=None):
        shift = self.get_object()
        port_data = shift.port_data.all()
        serializer = PortDataSerializer(port_data, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def expedition_data(self, request, pk=None):
        shift = self.get_object()
        expedition_data = shift.expedition_data.all()
        serializer = ExpeditionDataSerializer(expedition_data, many=True)
        return Response(serializer.data)

class BroyeurDataViewSet(viewsets.ModelViewSet):
    queryset = BroyeurData.objects.all()
    serializer_class = BroyeurDataSerializer
    permission_classes = [permissions.IsAuthenticated]

class SecheurDataViewSet(viewsets.ModelViewSet):
    queryset = SecheurData.objects.all()
    serializer_class = SecheurDataSerializer
    permission_classes = [permissions.IsAuthenticated]

class PortDataViewSet(viewsets.ModelViewSet):
    queryset = PortData.objects.all()
    serializer_class = PortDataSerializer
    permission_classes = [permissions.IsAuthenticated]

class ExpeditionDataViewSet(viewsets.ModelViewSet):
    queryset = ExpeditionData.objects.all()
    serializer_class = ExpeditionDataSerializer
    permission_classes = [permissions.IsAuthenticated]
