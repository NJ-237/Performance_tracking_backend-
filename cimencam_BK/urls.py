"""
URL configuration for cimencam_BK project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework.authtoken import views
from rest_framework import routers, serializers, viewsets
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from authentication.views import UserlistsViewSet,CustomAuthToken
# from django.conf.urls import url 

from authentication.apps import AuthenticationConfig
from authentication.serializers import RegisterSerializer
from authentication.views import  UserViewSet, ProfileGenericAPIView, ShiftViewSet, RoleList




# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'userslist', UserlistsViewSet, basename='user')
router.register(r'api/register', UserViewSet, basename='user_reg')
router.register(r'shifts', ShiftViewSet , basename='shift-list') 
router.register(r'role_drop', RoleList, basename='role_drop')


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('authentication.urls')),  # <-- this includes your shifts, broyeur, etc.
    # path('api/', include(router.urls)),  # <-- keeps the users route
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
     
    # Profile url
    #  path('api/', include(router.urls)),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api-token-auth/', views.obtain_auth_token),
    path('api-token-auth/', CustomAuthToken.as_view(), name='custom_token'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/profile/<pk>', ProfileGenericAPIView.as_view(), name='generic-api'),

]
# urlpatterns+=router.urls