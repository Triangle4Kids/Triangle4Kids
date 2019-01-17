import django_filters
from .models import Event

class EventFilter(django_filters.FilterSet):

    class Meta:
        model = Event
        fields = {
            # 'type_choice': ['icontains'],
            'age_choice': ['exact'],
            'class_camp_choice': ['exact'],
            'cities_choice': ['exact'],
        }

class EventFilterTextSearch(django_filters.FilterSet):

    class Meta:
        model = Event
        fields = {
            # 'title': ['icontains'],
            # 'description': ['icontains'],
            'type_choice': ['icontains'],
        }
     
    #  We want both search types on the index page:
    # 1) Preset toggle search for the 4 choices--> leads to a new search result page of events
    # 2) Full textfield search--> leads to a new search result page of businesses


#Order of search priorities:

# 1) Full text search on index page for every attribute in Businesses
#   ( and Events) NOT NOW
# and on /business page DONE
    # Can we make a text search that combines businesses and events? NO FOR NOW
# 2) Search by type-choice categories (ideally by clicking a button with category name)
    # same for camp/class/homeschool, and cities
    # same for /business page--make sidebar with Cities and Categories return a results page, add text search to top of page
# 3) Search by ratings (rank from highest to lowest)
    # pull-down menu on business page has search options--can we make this work
