from django.urls import path , include
from . import views
from rest_framework.routers import DefaultRouter
from .views import ShiftViewSet, Dryer_productionViewSet, Mill_productionViewSet, EquipementViewSet, ExpeditionDataViewSet


# from rest_framework.authtoken import views
from .views import CustomAuthToken, UserViewSet


router = DefaultRouter()
router.register(r'shifts', ShiftViewSet , basename='shift') 
router.register(r'Dryer_production', Dryer_productionViewSet, basename='Dryer_production')
router.register(r'Mill_production', Mill_productionViewSet, basename='Mill_production')
router.register(r'Equipement', EquipementViewSet, basename=' Equipement')
router.register(r'expedition-data', ExpeditionDataViewSet, basename='expedition-data')
router.register(r'users', UserViewSet, basename='users') # <-- Add the UserViewSet to this router

urlpatterns = [
    path('register/', views.register_user),
    # path('login/', views.login_user),
    # path('shift/' include)
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    # path('api-token-auth/', views.obtain_auth_token),

    # path('api-token-auth/', CustomAuthToken.as_view())
    path('login/', CustomAuthToken.as_view(), name='login'),


    # path('test/', views.test_endpoint, name='test-endpoint'),
    # path('shifts/', views.ShiftListCreate.as_view(), name='shift-list'),
    # path('shifts/<int:pk>/', views.ShiftDetail.as_view(), name='shift-detail'),
    # path('broyeur-data/', views.BroyeurDataListCreate.as_view(), name='broyeur-data-list'),
    # path('broyeur-data/<int:pk>/', views.BroyeurDataDetail.as_view(), name='broyeur-data-detail'),
    # path('secheur-data/', views.SecheurDataListCreate.as_view(), name='secheur-data-list'),
    # path('port-data/', views.PortDataListCreate.as_view(), name='port-data-list'),
    # path('expedition-data/', views.ExpeditionDataListCreate.as_view(), name='expedition-data-list'),
    # path('test/', views.test_endpoint, name='test-endpoint'),
    # Add your other endpoints...
]


