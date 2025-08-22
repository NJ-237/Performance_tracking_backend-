from django.urls import path , include
from . import views
from rest_framework.routers import DefaultRouter
from .views import ShiftViewSet, BroyeurDataViewSet, SecheurDataViewSet, PortDataViewSet, ExpeditionDataViewSet



router = DefaultRouter()
router.register(r'shifts', ShiftViewSet)
router.register(r'broyeur-data', BroyeurDataViewSet)
router.register(r'secheur-data', SecheurDataViewSet)
router.register(r'port-data', PortDataViewSet)
router.register(r'expedition-data', ExpeditionDataViewSet)

urlpatterns = [
    path('register/', views.register_user),
    path('login/', views.login_user),
    path('', include(router.urls)),
]
