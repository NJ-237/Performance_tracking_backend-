from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
# from django.contrib.auth import login
from .serializers import RegisterSerializer                       
from rest_framework import viewsets, permissions, status
from .models import Shift, Dryer_production, Equipement, Mill_production, ExpeditionData
from .serializers import ShiftSerializer, Dryer_productionSerializer, Mill_productionSerializer, EquipementSerializer, ExpeditionDataSerializer



from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.models import User  #new 
from rest_framework import serializers, viewsets # new



# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(['POST'])
def register_user(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# def login_user(request):
#     serializer = LoginSerializer(data=request.data)
#     print(request.data, serializer.is_valid())
#     if serializer.is_valid():
#         user = serializer.validated_data
#         print("blocked")
#         login(request, user)
#         return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
#     if not serializer.is_valid():
#         print(serializer.errors)
#         # return Response(serializer.errors, status=400)

#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

   

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
   


class ExampleView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
        }
        return Response(content)
     

# Create your views here.

# views.py for the input values from the ReportSide 

class ShiftViewSet(viewsets.ModelViewSet):

    # API endpoint for managing shifts.
         
    queryset = Shift.objects.all()
    serializer_class = ShiftSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['get'])
    def Mill_production(self, request, pk=None):
        shift = self.get_object()
        Mill_production = shift.Mill_production.all()
        serializer = Mill_productionSerializer(Mill_production, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def Equipement(self, request, pk=None):
        shift = self.get_object()
        Equipement = shift.Equipement.all()
        serializer = EquipementSerializer(Equipement, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def Dryer_production(self, request, pk=None):
        shift = self.get_object()
        Dryer_production = shift.Dryer_production.all()
        serializer = Dryer_productionSerializer(Dryer_production, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def expedition_data(self, request, pk=None):
        shift = self.get_object()
        expedition_data = shift.expedition_data.all()
        serializer = ExpeditionDataSerializer(expedition_data, many=True)
        return Response(serializer.data)

class Dryer_productionViewSet(viewsets.ModelViewSet):
    queryset = Dryer_production.objects.all()
    serializer_class = Dryer_productionSerializer
    permission_classes = [permissions.IsAuthenticated]

class EquipementViewSet(viewsets.ModelViewSet):
    queryset = Equipement.objects.all()
    serializer_class = EquipementSerializer
    permission_classes = [permissions.IsAuthenticated]

class Mill_productionViewSet(viewsets.ModelViewSet):
    queryset = Mill_production.objects.all()
    serializer_class = Mill_productionSerializer
    permission_classes = [permissions.IsAuthenticated]

class ExpeditionDataViewSet(viewsets.ModelViewSet):
    queryset = ExpeditionData.objects.all()
    serializer_class = ExpeditionDataSerializer
    permission_classes = [permissions.IsAuthenticated]
