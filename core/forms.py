from django.forms import ModelForm
from core.models import LeaveReview, Event, EVENT_TYPE, AGE_RANGE, CLASS_CAMP, CITIES
from django import forms


class LeaveReviewForm(ModelForm):
    class Meta:
        model = LeaveReview
        fields = ['title', 'event', 'rating', 'text']


class EventForm(forms.Form):
    title = forms.CharField(max_length=255)
    business = forms.CharField(max_length=255)
    # image = forms.ImageField(upload_to='test_image', blank=True)
    description = forms.CharField(max_length=255)
    link = forms.URLField()
    start_date = forms.DateField()
    end_date = forms.DateField()
    # null=True for end_date? Would differ from model.
    start_time = forms.TimeField()
    end_time = forms.TimeField()
    # type_choice = forms.MultipleChoiceField(choices=EVENT_TYPE)
    # age_choice = forms.CharField(
    #     max_length=20, choices=AGE_RANGE)
    # class_camp_choice = forms.CharField(
    #     max_length=10, choices=CLASS_CAMP)
    # address = forms.CharField(max_length=255)
    # cities_choice = forms.CharField(
    #     max_length=30, choices=CITIES)
