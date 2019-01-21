from django.forms import ModelForm
from core.models import LeaveReview, Event, EVENT_TYPE, AGE_RANGE, CLASS_CAMP, CITIES
from django import forms


class LeaveReviewForm(ModelForm):
    class Meta:
        model = LeaveReview
        fields = ['title', 'event', 'rating', 'text']


class EventForm(forms.Form):
    title = forms.CharField(label='Title', max_length=255)
    business = forms.CharField(label='Name of your business', max_length=255)
    # image = forms.ImageField(upload_to='test_image', blank=True)
    description = forms.CharField(label='Description', max_length=255)
    link = forms.URLField(label='Link')
    start_date = forms.DateField(label='Start Date')
    end_date = forms.DateField(label='End Date')
    # null=True for end_date? Would differ from model.
    start_time = forms.TimeField(label='Start Time')
    end_time = forms.TimeField(label='End Time')
    # type_choice = forms.MultipleChoiceField(choices=EVENT_TYPE)
    # age_choice = forms.CharField(
    #     max_length=20, choices=AGE_RANGE)
    # class_camp_choice = forms.CharField(
    #     max_length=10, choices=CLASS_CAMP)
    # address = forms.CharField(max_length=255)
    # cities_choice = forms.CharField(
    #     max_length=30, choices=CITIES)
