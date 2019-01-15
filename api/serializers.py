from django.db import models
from rest_framework import serializers
from core.models import Event, Business, Profile, LeaveReview


class BusinessSerializer(serializers.ModelSerializer):

    class Meta:
        model = Business
        fields = ('name', 'address', 'city', 'state', 'average_rating', 'link')




# class ProfileSerializer(serializers.ModelSerializer):


# class LeaveReviewSerializer(serializers.ModelSerializer):




# class EventSerializer(serializers.ModelSerializer):




