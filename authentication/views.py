from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.decorators import action
# from django.contrib.auth import login
from .serializers import UserSerializer,ProfileSerializer, UserLoginSerializer, Port_productionSerializer                   
from rest_framework import viewsets, permissions, status
from .models import Shift, Dryer_production, Equipement, Mill_production, ExpeditionData, Port_production, Feedback, Performance
from .serializers import ShiftSerializer, Dryer_productionSerializer, Mill_productionSerializer, EquipementSerializer, ExpeditionDataSerializer, FeedbackSerializer, PerformanceSerializer
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
# from django.contrib.auth import logout
# from .filters import ProductionFilter
# from django_filters.rest_framework import DjangoFilterBackend
from datetime import datetime
from rest_framework import generics
from django.db.models import Sum, Avg
from datetime import datetime, date
from django.shortcuts import get_object_or_404
from django.http import JsonResponse 
import pandas as pd

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
    

Debit_broyeur = 140,
Debit_secheur = 50

SHIFT_HOURS = {
    "shift1": 6,
    "shift2": 7,
    "shift3": 9
}
# class ProductionAggregateView(APIView):
#     queryset = Performance.objects.all()
#     serializer_class = PerformanceSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request, *args, **kwargs):
#         start_date_str = self.request.query_params.get('start_date')
#         end_date_str = self.request.query_params.get('end_date')

#         # Convert string dates to date objects
#         start_date = None
#         end_date = None
#         try:
#             if start_date_str:
#                 start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
#             if end_date_str:
#                 end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
#         except ValueError:
#             return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)

#         # 1. Filter the Shift records
#         shift_queryset = Shift.objects.all()
#         if start_date:
#             # Filter shifts where created_at is greater than or equal to the start date
#             shift_queryset = shift_queryset.filter(created_at__date__gte=start_date)
#         if end_date:
#             # Filter shifts where created_at is less than or equal to the end date
#             shift_queryset = shift_queryset.filter(created_at__date__lte=end_date)
            
#         # Get the IDs of the filtered shifts
#         filtered_shift_ids = shift_queryset.values_list('id', flat=True)
        
#         # 2. Aggregate Mill Production (Assuming one record per mill per shift is not possible
#         # with the current model structure, we'll SUM ALL production)
#         mill_data = Mill_production.objects.filter(shift_id__in=filtered_shift_ids).aggregate(
#             total_production=Sum('production'),
#             # You might aggregate other fields here like sum of clinker_Difference
#         )
#         # Simplify assumption: All 'production' is distributed equally to BK1, BK4, BK5. 
#         total_mill_production = mill_data.get('total_production') or 0
#         denominator = SHIFT_HOURS * Debit_broyeur
#         # mill_kpi_value = total_mill_production / 3 if total_mill_production > 0 else 0

#         if denominator != 0:
#             mill_kpi_value = 7 * (total_mill_production / denominator) < 14
#         else:
#             mill_kpi_value = 0

#         # BK1_kpi_value = mill_kpi_value
#         # BK4_kpi_value = mill_kpi_value
#         # BK5_kpi_value = mill_kpi_value

#         # 3. Aggregate Dryer Production (Secheur)
#         dryer_data = Dryer_production.objects.filter(shift_id__in=filtered_shift_ids).aggregate(
#             total_secheur_production=Sum('production'),
#             # avg_humidity_in=Avg('humidites_entree')
#         )
#         total_secheur_production = dryer_data.get('total_secheur_production') or 0
#         denominator1 = SHIFT_HOURS * Debit_secheur

#         if denominator != 0:
#             dryer_kpi_value = 6 * (total_secheur_production / denominator1) < 6
#         else:
#             dryer_kpi_value = 0

#         total_optimisation = (total_mill_production + total_secheur_production) * 0.05 
     
#         total_performance_percent = 85.5 

#         # 5. Build the final response
#         response_data = {
#             # KPIs
#             "total_optimisation": f"{total_optimisation:.2f}",
#             "total_performance": f"{total_performance_percent:.1f}",
            
#             # Mill/Dryer Production Totals
#             "production_bk1": f"{mill_kpi_value:.2f}",
#             "production_bk4": f"{mill_kpi_value:.2f}",
#             "production_bk5": f"{mill_kpi_value:.2f}",
#             "production_secheur": f"{dryer_kpi_value:.2f}",
            
#             "chart_data": [], 
#         }
#         print(response_data)
#         return Response(response_data)
#         # except Exception as e:
#         #         # Handle any exceptions that occur during execution
#         #         return JsonResponse({"error": str(e)}, status=500)

# class OperatorPerformanceHistoryView(APIView):
#     def get(self, request, operator_id): # <-- Accepts operator_id
#         # 1. Fetch the operator to ensure they exist
#         operator = get_object_or_404(User, pk=Profile)

#         # 2. Filter performance data for that operator
#         queryset = Mill_production.objects.filter(operator=operator).order_by('shift_date', 'shift_number')
        
#         # 3. Format the data for Chart.js
#         labels = []          # X-axis: Shift/Date identifier
#         Blaines = []      # Data 1: Efficiency values
#         production = []      # Data 2: Production values
        
#         for record in queryset:
#             labels.append(f"{record.shift_date.strftime('%m-%d')} ({record.shift_number})")
#             Blaines.append(record.efficiency_percent)
#             production.append(record.production_output)

#         response_data = {
#             'operator_name': operator.name,
#             'labels': labels,
#             'efficiency_data': Blaines,
#             'production_data': production,
#         }
        
#         return Response(response_data)

class  ProductionKPIView(APIView):
    def get(self, request, *args, **kwargs):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        exact_date = request.query_params.get('date')

        queryset = Mill_production.objects.all()

        # 🔹 Filter by related Shift.created_at field
        if start_date and end_date:
            queryset = queryset.filter(shift__created_at__date__range=[start_date, end_date])
        elif start_date:
            queryset = queryset.filter(shift__created_at__date__gte=start_date)
        elif end_date:
            queryset = queryset.filter(shift__created_at__date__lte=end_date)
        elif exact_date:
            queryset = queryset.filter(shift__created_at__date=exact_date)

        # 🔹 Aggregate totals for mill
        mill_data = queryset.aggregate(
            total_arret_incident=Sum('arret_par_incident'),
            total_production=Sum('production')
        )

        arret_value = mill_data.get('total_arret_incident') or 0
        production_value = mill_data.get('total_production') or 0

        # 🔹 KPI Computations
        CIBLE_ARRET = 10
        CIBLE_PRI = 30

        arret_par_incident = min(10, 10 * (arret_value / CIBLE_ARRET)) if CIBLE_ARRET else 0
        PRI = min(30, 30 * (production_value / CIBLE_PRI)) if CIBLE_PRI else 0

        total_production_value = arret_par_incident + PRI


        # 🔹 Aggregate totals for optimization
        mill_data = queryset.aggregate(
            total_HNA=Sum('HNA'),
            total_Ecart_type=Sum('Ecart_type'),
            total_Blaines=Sum('Blaines'),
            total_temp=Sum('temp')
        )

        HNA_value = mill_data.get('HNA') or 0
        Ecart_type_value = mill_data.get('total_Ecart_type') or 0
        Blaines_value = mill_data.get('total_Blaines') or 0
        temp_value = mill_data.get('total_temp') or 0
        # 🔹 KPI Computations
        CIBLE_HNA = 15
        CIBLE_Ecart_type = 15
        CIBLE_Blaines = 20
        CIBLE_temp = 10

        HNA = min(15, 15 * (HNA_value / CIBLE_HNA)) if CIBLE_HNA else 0
        Ecart_type = min(15, 15 * (Ecart_type_value / CIBLE_Ecart_type)) if CIBLE_Ecart_type else 0
        Blaines = min(15, 15 * (Blaines_value / CIBLE_Blaines)) if CIBLE_Blaines else 0
        temp = min(15, 15 * (temp_value / CIBLE_temp)) if CIBLE_temp else 0

        total_qualites_value = Blaines + temp
        total_optimisation_value = HNA + Ecart_type
        
        
        return Response({
            "arret_par_incident": round(arret_par_incident, 2),
            "PRI": round(PRI, 2),
            "total_production": round(total_production_value, 2),
            "HNA": round(HNA, 2),
            "Ecart_type": round(Ecart_type, 2),
            "total_optimisation": round(total_optimisation_value, 2),
            "Blaines": round(Blaines, 2),
            "temp": round(temp, 2),
            "total_qualites": round(total_qualites_value, 2)
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
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        print('all')
        serializer.save(created_by=self.request.user.profile)


@action(detail=True, methods=['get'])
def Dryer_data(self, request, pk=None):
        shift = self.get_object()
        Dryer_data = shift.Dryer_data.all()
        serializer = Dryer_productionSerializer(Dryer_data, many=True)
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
   

    def perform_create(self, serializer):
        print('all', self.request)
        print(self.get_object, self.request.data)
        serializer.save()
        # serializer.save(created_by=self.request.user.profile)


# class EquipementViewSet(viewsets.ModelViewSet):
#     queryset = Equipement.objects.all()
#     serializer_class = EquipementSerializer
#     permission_classes = [permissions.IsAuthenticated]

class Mill_productionViewSet(viewsets.ModelViewSet):
    queryset = Mill_production.objects.all()
    serializer_class = Mill_productionSerializer

    def perform_create(self, serializer):
        print('all', self.request)
        print(self.get_object, self.request.data)
        serializer.save()
    permission_classes = [permissions.IsAuthenticated]

   

class ExpeditionDataViewSet(viewsets.ModelViewSet):
    queryset = ExpeditionData.objects.all()
    serializer_class = ExpeditionDataSerializer
    permission_classes = [permissions.IsAuthenticated]
    # def perform_create(self, serializer):
#         # We access the authenticated user's related Profile object.
#         # This assumes your User model has a one-to-one relationship with a Profile model
#         # defined as a related name like `user.profile`.
        # serializer.save(created_by=self.request.user.profile)
    

class Port_productionViewSet(viewsets.ModelViewSet):
    queryset = Port_production.objects.all()
    serializer_class = Port_productionSerializer

    def perform_create(self, serializer):
        print('all', self.request)
        print(self.get_object, self.request.data)
        serializer.save()
    permission_classes = [permissions.IsAuthenticated]


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

    def perform_create(self, serializer):
        print('all', self.request)
        print(self.get_object, self.request.data)
        serializer.save()
    permission_classes = [permissions.IsAuthenticated]
 



# class PerformanceViewSet(viewsets.ModelViewSet):
#     queryset = Performance.objects.all()
#     serializer_class = PerformanceSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request, *args, **kwargs):
#         try:
#             mill_data = Mill_production.objects.filter().aggregate(
#                     total_production=Sum('production'),
#                 )
  
#             total_mill_production = mill_data.get('total_production') or 0
#             denominator = SHIFT_HOURS * Debit_broyeur

#             if denominator != 0:
#                 BK_kpi_value = 7 * (total_mill_production / denominator)
#             else:
#                 BK_kpi_value = 0

#             BK1_kpi_value = BK_kpi_value
#             BK4_kpi_value = BK_kpi_value
#             BK5_kpi_value = BK_kpi_value
               
# #               For dryer / secheur
#             dryer_data = Dryer_production.objects.filter().aggregate(
#                     total_production=Sum('production'),
#                 )
  
#             total_dryer_production = dryer_data.get('total_production') or 0
#             denominator1 = SHIFT_HOURS * Debit_secheur

#             if denominator != 0:
#                 dryer_kpi_value = 6 * (total_dryer_production / denominator1)
#             else:
#                 dryer_kpi_value = 0
            

#             my_data = {
#                 "total_production": total_mill_production,
#                 "BK1_KPI": BK1_kpi_value,
#                 "BK4_KPI": BK4_kpi_value,
#                 "BK5_KPI": BK5_kpi_value,
#                 "Dryer_KPI": dryer_kpi_value,
#                 "debit_broyeur_rate": Debit_broyeur,
#                 "debit_secheur_rate": Debit_secheur 
#             }
#             print(my_data)
#             return JsonResponse(my_data)

#         except Exception as e:
#             # Handle any exceptions that occur during execution
#             return JsonResponse({"error": str(e)}, status=500)

