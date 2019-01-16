from django.db import models 
from rest_framework import serializers
from core.models import Event, Business, Profile, LeaveReview, BusinessLatLong


class BusinessSerializer(serializers.ModelSerializer):

    class Meta:
        model = Business
        fields = ('name', 'address', 'city', 'state', 'average_rating', 'link')


class BusinessLatLongSerializer(serializers.ModelSerializer):

    class Meta:
        model = BusinessLatLong
        fields = ('latitude', 'longitude', 'relevance', 'location_name', 'business')         