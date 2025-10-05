import django_filters
from .models import Mill_production, Dryer_production

class ProductionFilter(django_filters.FilterSet):
     start_date = django_filters.DateFilter(
        field_name='shift__date', 
        lookup_expr='gte',
        label='Production Start Date'
    )
     end_date = django_filters.DateFilter(
        field_name='shift__date', 
        lookup_expr='lte',
        label='Production End Date'
    )

class Meta:
        # This FilterSet will be applied to Dryer, Secheur, and Mill
        model = Dryer_production, Mill_production,  # Can be any of the production models for definition purposes
        fields = ['start_date', 'end_date']