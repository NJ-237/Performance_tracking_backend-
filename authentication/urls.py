from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework import routers
from django.urls import path, include

# Routers provide an easy way of automatically determining the URL conf.
#For URL config with viewset 
router = routers.DefaultRouter()

router.register(r'register',views.UserViewSet,basename='user_reg')
router.register(r'shifts',views.ShiftViewSet,basename='shift_list')
router.register(r'expedition',views.ExpeditionDataViewSet,basename='expedition_list')
router.register(r'mill',views.Mill_productionViewSet,basename='mill_list')
router.register(r'dryer',views.Dryer_productionViewSet,basename='dryer_list')
router.register(r'equipement',views.EquipementViewSet,basename='equipment_list')


#For URL Configurations with Class-Based API View 
urlpatterns = [
    path("login/", views.LoginAPIView.as_view(),name='login'),
    path("role_drop/", views.RoleList.as_view(),name='role_drop'),
    path("token_auth/", views.CustomAuthToken.as_view(),name='custom_token'),
    path("token/refresh", TokenRefreshView.as_view(),name='token_refresh'),
    path("profile/<pk>", views.ProfileGenericAPIView.as_view(),name='profile'),
    path("logout/", views.LogoutView.as_view(),name='logout'),
    path("", include(router.urls)),
]   


