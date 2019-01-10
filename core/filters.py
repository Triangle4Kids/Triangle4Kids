import django_filters
from .models import Event

class EventFilter(django_filters.FilterSet):
    # research lookup expressions
    # name = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Event
        fields = {
            'title': ['icontains'],
            'type_choice': ['icontains'],
            'age_choice': ['icontains'], 'class_camp_choice': ['icontains'], 'cities_choice': ['icontains']
        }
     # test these, then add start_date, start_time, discuss what else)