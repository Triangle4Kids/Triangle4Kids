import django_filters
from .models import Event

class EventFilter(django_filters.FilterSet):
    # research lookup expressions
    # name = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Event
        fields = [
            # 'type_choice',
            # type_choice 
            'age_choice',
            'class_camp_choice',
            'cities_choice',
        ]

class EventFilterTextSearch(django_filters.FilterSet):

    class Meta:
        model = Event
        fields = {
            'title': ['icontains'],
            'description': ['icontains'],
            # 'type_choice': ['icontains'],
        }
     # test these, then add start_date, start_time, discuss what else)