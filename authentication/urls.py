from django.urls import path , include
from . import views
from rest_framework.routers import DefaultRouter
from .views import ShiftViewSet, Dryer_productionViewSet, Mill_productionViewSet, EquipementViewSet, ExpeditionDataViewSet

from .views import CROListAPIView, LoginAPIView, RoleList

# from rest_framework.authtoken import views
from .views import CustomAuthToken
from .views import UserlistsViewSet ,UserViewSet


router = DefaultRouter()
# router.register(r'Dryer_production', Dryer_productionViewSet, basename='Dryer_production')
# router.register(r'Mill_production', Mill_productionViewSet, basename='Mill_production')
# router.register(r'Equipement', EquipementViewSet, basename=' Equipement')
# router.register(r'expedition-data', ExpeditionDataViewSet, basename='expedition-data')
# router.register(r'users', UserViewSet, basename='users') # <-- Add the UserViewSet to this router
# router.register(r'userlist', UserlistsViewSet, basename='userlist') # <-- Add the Userlist to this router

urlpatterns = [
    # path('register/', views.register_user),
    # path('login/', views.login_user),
 
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    # path('api-token-auth/', views.obtain_auth_token),

    # path('api-token-auth/', CustomAuthToken.as_view())
    # path('login/', CustomAuthToken.as_view(), name='login'),

     # API for getting the list of CROs for the dropdown
    path('cros/', CROListAPIView.as_view(), name='cro-list'),
     # API for user login
    path('login/', LoginAPIView.as_view(), name='login'),

    # # path('userlist/', include('UserlistsViewSet.urls'), name='userlist'),
    # path('userlist/', views.UserlistsViewSet.as_view(), name='userlist'),
    path('shift/', views.ShiftViewSet.as_view, name='shift-list'),
    path('role_drop/', RoleList.as_view(), name='role_drop'),
    path('register/', UserViewSet.as_view, name='user_reg'),

]


