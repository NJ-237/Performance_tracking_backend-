from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
# from django.contrib.auth import login
from .serializers import RegisterSerializer                       
from rest_framework import viewsets, permissions, status, generics
from .models import Shift, Dryer_production, Equipement, Mill_production, ExpeditionData
from .serializers import ShiftSerializer, Dryer_productionSerializer, Mill_productionSerializer, EquipementSerializer, ExpeditionDataSerializer
#new
from django.contrib.auth import authenticate, get_user_model
from .models import Profile
from .serializers import ProfileSerializer, UserLoginSerializer

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView


from rest_framework.authtoken.models import Token
from rest_framework.renderers import JSONRenderer,TemplateHTMLRenderer
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.models import User  #new 
from rest_framework import serializers, viewsets # new
import django_filters.rest_framework





class RoleList(GenericAPIView):
    queryset = Profile.objects.all()
    # profileset=queryset.user.all()
    # serializer_class = ProfileSerializer
    # lookup_field = 'username'
    # lookup_url_kwarg = None

    def get(self, request, *args, **kwargs):
        # print(self.profileset)
        croqueryset = self.queryset.filter(role="CRO").values('user__id', 'user__username') # Get queryset
        patrollerqueryset = self.queryset.filter(role="Patroller").values('user__id', 'user__username') # Get queryset
        cdqqueryset=self.queryset.filter(role="CDQ").values('user__id', 'user__username') # Get queryset
        # serializer = self.get_serializer(queryset, many=True)  # Serialize queryset
        # print(serializer.data)
        # pat_serial = self.get_serializer(patrollerqueryset, many=True)  # Serialize queryset
        # cdq_serial = self.get_serializer(cdqqueryset, many=True)  # Serialize queryset

        # return Response({"CRO":serializer.data,"Patroller":pat_serial.data,"CDQ":cdq_serial.data})
        return Response({
            "CRO": croqueryset,
            "Patroller": patrollerqueryset,
            "CDQ": cdqqueryset
        })



User = get_user_model()

# Serializers define the API representation.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"



class LoginAPIView(APIView):
    """
    Handles user login.
    Returns a token and the user's role upon successful authentication.
    """
    serializer_class = UserLoginSerializer
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user:
            # Check if user has a related Profile
            try:
                profile = Profile.objects.get(user=user)
                role = profile.Position.lower()
            except Profile.DoesNotExist:
                # Handle case where user has no profile
                role = 'unknown' 

            # Get or create the auth token for the user
            token, created = Token.objects.get_or_create(user=user)

            return Response({
                'token': token.key,
                'user': user,
                'username': user.username,
            }, status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )


class CROListAPIView(generics.ListAPIView):
    """
    API view to list all registered CROs.
    Only allows authenticated users to access this list.
    """
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Filter the queryset to return only profiles with the 'cro' position.
        The filter is case-insensitive.
        """
        return Profile.objects.filter(Position__iexact='cro')
    

class  ProfileGenericAPIView(GenericAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'pk'
    lookup_url_kwarg = None

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()  # Get queryset
        serializer = self.get_serializer(queryset, many=True)  # Serialize queryset
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
            data = request.data # Get queryset
            object = self.get_object()
            serializer = self.get_serializer(object, data, partial=True)  # Serialize queryset
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response(serializer.data)





# # ViewSets define the view behavior.
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# @api_view(['POST'])
# def register_user(request):
#     serializer = RegisterSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        # serializer = self.serializer_class(data=request.data,
        #                                    context={'request': request})
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        serializer=UserSerializer(user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': serializer.data,
        })

#Endpoints to list all the users.
class UserlistsViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    #  @action(detail=True, methods=['get'])
    def get(self, request,format=None):
        pass

#Endpoitns for dropdowns : 
# from .filter import Rolefilter
# class  RolefilterViewSet(viewsets.ModelViewSet):
      
#     queryset = Profile.objects.all()
#     serializer_class = ProfileSerializer
#     filterset_class =  Rolefilter


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
