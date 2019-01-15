from django.shortcuts import render
from rest_framework import viewsets, filters
from api.serializers import BusinessSerializer
from core.models import Business
from django_filters.rest_framework import DjangoFilterBackend


class BusinessViewset(viewsets.ModelViewSet):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name')


