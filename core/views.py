from django.shortcuts import render
from django.contrib.auth.forms import PasswordChangeForm
from core.models import Event, Business, LeaveReview, Profile
from core.forms import LeaveReviewForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.


def index(request):
    events = Event.objects.all()
    businesses = Business.objects.all()
    return render(request, 'index.html', {
        "events": events,
        "businesses": businesses,
    })


def new_index(request):
    events = Event.objects.all()
    businesses = Business.objects.all()
    return render(request, 'bsindex.html', {
        "events": events,
        "businesses": businesses,
    })


def business_directory(request):
    businesses = Business.objects.all()
    return render(request, 'business/business_directory.html', {
        "businesses": businesses,
    })


def event_detail(request, slug):
    event = Event.objects.get(slug=slug)
    is_favorite = False

    if event.favorite.filter(id=request.user.id).exists():
        is_favorite = True

    return render(request, 'events/event_detail.html', {
        'event': event,
        'is_favorite': is_favorite,
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
           return redirect('home')

   review = LeaveReview.objects.filter(business=business)

   return render(request, 'business/business_detail.html', {
       'business': business,
       'events': events,
       'form': form,
       'review': review,
   })  

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
    return render(request, 'user_account.html', {
        'reviews': reviews,
        'favorite_event': favorite_event,
    })


def favorite_event(request, id):
    event = get_object_or_404(Event, id=id)
    if event.favorite.filter(id=request.user.id).exists():
        event.favorite.remove(request.user)
    else:
        event.favorite.add(request.user)
    return redirect('home')


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
