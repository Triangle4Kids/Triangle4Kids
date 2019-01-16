from django.shortcuts import render
from rest_framework import viewsets, filters
from api.serializers import BusinessSerializer, BusinessLatLongSerializer
from core.models import Business, BusinessLatLong
from django_filters.rest_framework import DjangoFilterBackend

class BusinessViewset(viewsets.ModelViewSet):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name')



class BusinessLatLongViewset(viewsets.ModelViewSet):
    queryset = BusinessLatLong.objects.all()
    serializer_class = BusinessLatLongSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('business')
    

# Create your views here.
