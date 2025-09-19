from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.decorators import action
# from django.contrib.auth import login
from .serializers import UserSerializer,ProfileSerializer, UserLoginSerializer, Port_productionSerializer                   
from rest_framework import viewsets, permissions, status
from .models import Shift, Dryer_production, Equipement, Mill_production, ExpeditionData, Port_production
from .serializers import ShiftSerializer, Dryer_productionSerializer, Mill_productionSerializer, EquipementSerializer, ExpeditionDataSerializer
#new
from django.contrib.auth import authenticate
from .models import Profile
# Import the correct JWT views
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView


from rest_framework.authtoken.models import Token
from rest_framework.renderers import JSONRenderer,TemplateHTMLRenderer
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.models import User  #new 
from rest_framework import serializers, viewsets # new
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import logout



class RoleList(GenericAPIView):
    queryset = Profile.objects.all()

    def get(self, request, *args, **kwargs):
        # print(self.profileset)
        croqueryset = self.queryset.filter(role="CRO").values('user__id', 'user__username') # Get queryset
        patrollerqueryset = self.queryset.filter(role="Patroller").values('user__id', 'user__username') # Get queryset
        cdqqueryset=self.queryset.filter(role="CDQ").values('user__id', 'user__username') # Get queryset
       
        return Response({
            "CRO": croqueryset,
            "Patroller": patrollerqueryset,
            "CDQ": cdqqueryset
        })

class MyTokenObtainPairView(TokenObtainPairView):
    # This view is already configured to handle JWT token creation.
    # No need for a custom class unless you need to override its behavior.
    pass

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
                role = profile.role.lower()
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



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer



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

# Endpoints for the LogOut 
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Delete the user's token
        request.user.auth_token.delete()
        
        # Return a success response
        return Response(status=status.HTTP_200_OK)

class ShiftViewSet(viewsets.ModelViewSet):

    # API endpoint for managing shifts.
         
    queryset = Shift.objects.all()
    serializer_class = ShiftSerializer
    # permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        print('all')
        serializer.save(created_by=self.request.user.profile)

    
# @action(detail=True, methods=['get'])
# def Mill_production(self, request, pk=None):
#         shift = self.get_object()
#         Mill_production = shift.Mill_production.all()
#         serializer = Mill_productionSerializer(Mill_production, many=True)
#         return Response(serializer.data)

# @action(detail=True, methods=['get'])
# def Equipement(self, request, pk=None):
#         shift = self.get_object()
#         Equipement = shift.Equipement.all()
#         serializer = EquipementSerializer(Equipement, many=True)
# #         return Response(serializer.data)
# @action(detail=True, methods=['get'])
# def Dryer_data(self, request, pk=None):
#         shift = self.get_object()
#         Dryer_data = shift.Dryer_data.all()
#         serializer = Dryer_productionSerializer(Dryer_data, many=True)
#         return Response(serializer.data)
    
@action(detail=True, methods=['get'])
def expedition_data(self, request, pk=None):
        shift = self.get_object()
        expedition_data = shift.expedition_data.all()
        serializer = ExpeditionDataSerializer(expedition_data, many=True)
        return Response(serializer.data)

class Dryer_productionViewSet(viewsets.ModelViewSet):
    queryset = Dryer_production.objects.all()
    serializer_class = Dryer_productionSerializer

    def perform_create(self, serializer):
        print('all', self.request)
        print(self.get_object, self.request.data)
        serializer.save()
        # serializer.save(created_by=self.request.user.profile)
#     permission_classes = [permissions.IsAuthenticated]


# class EquipementViewSet(viewsets.ModelViewSet):
#     queryset = Equipement.objects.all()
#     serializer_class = EquipementSerializer
#     permission_classes = [permissions.IsAuthenticated]

# class Mill_productionViewSet(viewsets.ModelViewSet):
#     queryset = Mill_production.objects.all()
#     serializer_class = Mill_productionSerializer
#     permission_classes = [permissions.IsAuthenticated]

class ExpeditionDataViewSet(viewsets.ModelViewSet):
    queryset = ExpeditionData.objects.all()
    serializer_class = ExpeditionDataSerializer
#     permission_classes = [permissions.IsAuthenticated]
    # def perform_create(self, serializer):
#         # We access the authenticated user's related Profile object.
#         # This assumes your User model has a one-to-one relationship with a Profile model
#         # defined as a related name like `user.profile`.
        # serializer.save(created_by=self.request.user.profile)
    

# class Port_productionViewSet(viewsets.ModelViewSet):
#     queryset = Port_production.objects.all()
#     serializer_class = Port_productionSerializer
#     permission_classes = [permissions.IsAuthenticated]
