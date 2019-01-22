from django.shortcuts import render
from django.contrib.auth.forms import PasswordChangeForm
from core.models import Event, Business, LeaveReview, Profile, EVENT_TYPE, AGE_RANGE, CLASS_CAMP, CITIES, BusinessLatLong
from core.forms import LeaveReviewForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .filters import EventFilterTextSearch, EventFilter
from django.db.models import Avg, F
from django.contrib.postgres.search import SearchQuery, \
SearchRank, SearchVector
from django.views.generic import ListView
from rest_framework import viewsets, filters
from rest_framework.response import Response
from api.serializers import BusinessSerializer, BusinessLatLongSerializer
import json
from django.contrib import messages

# from .forms import SearchForm


class BusinessResultsListView(ListView):
    model = Business
    context_object_name = 'business_list'
    template_name = 'bsbusiness_directory.html'

    # paginate_by = 12

    def get_queryset(self):

        qs = Business.objects.all().annotate(avg_rating=Avg("reviews__rating"))

        keywords = self.request.GET.get('q')
        if keywords:
            query = SearchQuery(keywords)
            vector = SearchVector('name', 'address', 'city', 'state')
            qs = qs.annotate(search=vector).filter(search=query)
            qs = qs.annotate(
                rank=SearchRank(vector, query)).order_by('avg_rating')
        return qs


class EventResultsListView(ListView):
    model = Event
    context_object_name = 'event_list'
    template_name = 'bsevent_directory.html'

    def get_queryset(self):
        qs = Event.objects.all().order_by('start_date')
        return qs


def event_list_preset(request):
    f = EventFilter(request.GET, queryset=Event.objects.all())
    return render(
        request, 'bsevent_directory.html', {
            'filter': f,
            'type_choices': EVENT_TYPE,
            'age_choices': AGE_RANGE,
            'class_camp_choices': CLASS_CAMP,
            'cities_choices': CITIES
        })


def event_list_text(request):
    f = EventFilterTextSearch(request.GET, queryset=Event.objects.all())
    return render(request, 'events/event_list.html', {'filter': f})


def index(request):
    events = Event.objects.all()
    businesses = Business.objects.all().annotate(
        avg_rating=Avg("reviews__rating"))

    return render(request, 'bsindex.html', {
        "events": events,
        "businesses": businesses,
    })


def mapboxTest(request):
    events = Event.objects.all()
    businesses = Business.objects.all()
    return render(request, 'mapboxTest.html', {
        "events": events,
        "businesses": businesses,
    })


def mapBoxPlotTest(request):
    events = Event.objects.all()
    businesses = Business.objects.all()
    return render(request, 'mapBoxPlotTest.html', {
        "events": events,
        "businesses": businesses,
    })


def business_directory(request):
    businesses = Business.objects.all().annotate(
        avg_rating=Avg("reviews__rating")).order_by(
            F('avg_rating').desc(nulls_last=True))
    alpha_businesses = businesses.order_by('name')

    return render(request, 'bsbusiness_directory.html', {
        "businesses": businesses,
        "alpha_businesses": alpha_businesses,
    })


def event_directory(request):
    events = Event.objects.all()
    return render(request, 'bsevent_directory.html', {
        "events": events,
    })


def event_detail(request, slug):
    event = Event.objects.get(slug=slug)
    is_favorite = False

    business = event.business
    business_slug = event.business.slug
    business1 = Business.objects.annotate(
        avg_rating=Avg("reviews__rating")).get(slug=business_slug)

    if event.favorite.filter(id=request.user.id).exists():
        is_favorite = True

    return render(
        request, 'bsevent_detail.html', {
            'event': event,
            'is_favorite': is_favorite,
            'business': business,
            'business_slug': business_slug,
            'business1': business1,
        })


def business_detail(request, slug):
    business_review = Business.objects.annotate(
        avg_rating=Avg("reviews__rating")).get(slug=slug)
    events = business_review.events.all()
    user = request.user

    form = LeaveReviewForm()
    
    if request.method == "POST":
        if user.is_authenticated:
            form = LeaveReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.business_review = business_review
                review.reviewer = request.user
                review.save()
                return redirect('business_detail', slug=business_review.slug)
        else:
            messages.success(request, "Oops , must be logged in to review! ")

    review = LeaveReview.objects.filter(business_review=business_review)

    return render(
        request, 'bsbusiness_detail.html', {
            'business_review': business_review,
            'events': events,
            'form': form,
            'review': review,
        })


def newbusiness_detail(request, slug):
    business = Business.objects.annotate(
        avg_rating=Avg("reviews__rating")).get(slug=slug)
    events = business.events.all()

    form = LeaveReviewForm()

   
    if request.method == "POST":
        form = LeaveReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.business = business
            review.reviewer = request.user
            review.save()
            return redirect('newbusiness_detail', slug=business.slug)

    review = LeaveReview.objects.filter(business_review=business)
    # average_score = review.aggregate(Avg('rating'))

    return render(request, 'newbusinessdetail.html', {
        'business': business,
        'events': events,
        'form': form,
        'review': review,
    })


@login_required
def user_delete_review(request, id):
    user = request.user
    review = LeaveReview.objects.get(id=id)
    if (request.user == review.reviewer):
        review.delete()
    return redirect('get_user_profile')


@login_required
def get_user_profile(request):
    user = request.user

    reviews = LeaveReview.objects.filter(reviewer=user)
    favorite_event = user.favorite.all
   

    return render(request, 'bsuser_account.html', {
        'reviews': reviews,
        'favorite_event': favorite_event,
        
    })


def favorite_event(request, id):
    event = get_object_or_404(Event, id=id)

    if event.favorite.filter(id=request.user.id).exists():
        event.favorite.remove(request.user)
    else:
        event.favorite.add(request.user)
    return redirect('event_detail', slug=event.slug)


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('profile')
        else:
            return redirect('change_password')

    else:
        form = PasswordChangeForm(user=request.user)

        args = {'form': form}
        return render(request, 'profile/change_password.html', args)
