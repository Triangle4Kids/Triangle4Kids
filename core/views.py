from django.shortcuts import render
from django.contrib.auth.forms import PasswordChangeForm
from core.models import Event, Business, LeaveReview, Profile
from core.forms import LeaveReviewForm, CViewerForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .filters import EventFilterTextSearch, EventFilter

from django.db.models import Avg

from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.views.generic import ListView

# Trying to get City selection working
def get_city(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CViewerForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CViewerForm()

    return render(request, '##.html', {'form': form})


class BusinessResultsListView(ListView):
    model = Business
    context_object_name = 'business_list'
    template_name = 'bsbusiness_directory.html'

    def get_queryset(self):

        qs = Business.objects.all()

        keywords = self.request.GET.get('q')
        if keywords:
            query = SearchQuery(keywords)
            vector = SearchVector(
                'name', 'address', 'city', 'state'
            )
            qs = qs.annotate(search=vector).filter(search=query)
            qs = qs.annotate(rank=SearchRank(vector, query)).order_by('-average_rating')
        return qs


# def get_queryset(self):
#     queryset = Business.average_rating.all()
#     return super().get_queryset()


def event_list_preset(request):
    f = EventFilter(request.GET, queryset=Event.objects.all())
    return render(request, 'events/event_list.html', {'filter': f})


def event_list_text(request):
    f = EventFilterTextSearch(request.GET, queryset=Event.objects.all())
    return render(request, 'events/event_list.html', {'filter': f})


# Testing Filter Buttons
# class CityForm(forms.Form):
#     do = forms.ChoiceField(
#         widget=MultipleSubmitButton,
#         choices=CITIES,
#     )

def index(request):
    events = Event.objects.all()
    businesses = Business.objects.all()
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
    businesses = Business.objects.all()
    return render(request, 'bsbusiness_directory.html', {
        "businesses": businesses,
    })


def event_detail(request, slug):
    event = Event.objects.get(slug=slug)
    is_favorite = False
    business = event.business
    business_slug = event.business.slug

    if event.favorite.filter(id=request.user.id).exists():
        is_favorite = True

    return render(
        request, 'bsevent_detail.html', {
            'event': event,
            'is_favorite': is_favorite,
            'business': business,
            'business_slug': business_slug,
        })


def business_detail(request, slug):
    business = Business.objects.get(slug=slug)
    events = business.events.all()

    form = LeaveReviewForm()

    if request.method == "POST":
        form = LeaveReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.business = business
            review.reviewer = request.user
            review.save()
            return redirect('business_detail', slug=business.slug)

    review = LeaveReview.objects.filter(business=business)
    average_score = review.aggregate(Avg('rating'))

    return render(
        request, 'bsbusiness_detail.html', {
            'business': business,
            'events': events,
            'form': form,
            'review': review,
            'average_score': average_score,
        })


# # MapBox #
# def default_map(request):
#     # TODO: move this token to Django settings from an environment variable
#     # found in the Mapbox account settings and getting started instructions
#     # see https://www.mapbox.com/account/ under the "Access tokens" section
#     mapbox_access_token = 'pk.eyJ1IjoidHJpYW5nbGU0a2lkcyIsImEiOiJjanFubWRwMGw3a2hjNGFtc3RrMWQ4OXl5In0.eZj0i5qyOBlmeY2oH6LWow'
#     return render(request, 'default.html',
#                   {'mapbox_access_token': mapbox_access_token})


@login_required
def user_delete_review(request, id):
    user = request.user
    review = LeaveReview.objects.filter(reviewer=user)

    review.delete()
    return redirect('home')


@login_required
def get_user_profile(request):
    user = request.user

    reviews = LeaveReview.objects.filter(reviewer=user)
    favorite_event = user.favorite.all()

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
