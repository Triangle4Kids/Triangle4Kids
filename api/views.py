from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, filters
from rest_framework.response import Response
from api.serializers import BusinessSerializer, BusinessLatLongSerializer, \
 EventSerializer, EventLatLongSerializer
from core.models import Business, BusinessLatLong, Event, EventLatLong
from django_filters.rest_framework import DjangoFilterBackend


class BusinessViewset(viewsets.ModelViewSet):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name')


class BusinessLatLongViewset(viewsets.ModelViewSet):
    queryset = BusinessLatLong.objects.all()
    serializer_class = BusinessLatLongSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('business')


class BusinessDetailViewset(viewsets.ModelViewSet):
    def get(self, request, pk):
        biz = get_object_or_404(BusinessLatLong, pk=pk)
        serializer_class = BusinessLatLongSerializer(biz)
        return Response(serializer_class.data)


class EventLatLongViewset(viewsets.ModelViewSet):
    queryset = EventLatLong.objects.all()
    serializer_class = EventLatLongSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('title')


class EventViewset(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('title')