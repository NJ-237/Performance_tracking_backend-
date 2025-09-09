import django_filters
from .models import Profile

class Rolefilter(django_filters.FilterSet):
    class Meta:
        model = Profile
        fields = {
            'role': ['exact'],
        }