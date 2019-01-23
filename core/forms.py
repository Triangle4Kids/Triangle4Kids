from django.forms import ModelForm
from core.models import LeaveReview, Event
# from uni_form.helper import FormHelper
from crispy_forms.helper import FormHelper
from django import forms


class LeaveReviewForm(ModelForm):
    class Meta:
        model = LeaveReview
        fields = [
            'title', 'event', 'rating', 'text',
        ]
        help_texts = {
            'text': 'Please note: All reviews are monitored. We encourage you to be honest, but please be considerate when reviewing businesses and remain from using any inappropriate language. Thanks!',
        }
        labels = {
            'title': "Title of Review : ( Example: \"The yoga is fun!\" ) ",
         'event': "Is there an Activity or Event you are reviewing?  ( Example: \" Yoga at the Goat Farm ...\" )", 
         'rating': "Rating: ( Please provide a rating between 1-5 ) ", 
         'text': "My Review: ( Let us know what you think! ) ",
         
         }


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = [
            'title', 'link', 'description', 'start_date', 'end_date', 'start_time', 'end_time', 'image', 'type_choice', 'age_choice', 'class_camp_choice', 'address', 'city', 'state',
        ]


class NewEventForm (forms.Form):
    name = forms.CharField(label='Your name', max_length=150)
    email = forms.EmailField()
    event_name = forms.CharField(label='Name of Event', max_length=200)
    business = forms.CharField(label='Event Business', max_length=100)
    description = forms.CharField(label='Event Description', max_length=600)
    event_location = forms.CharField(label='Location of Event', max_length=100)
    event_date = forms.CharField(label='Date of Event')
    start_time = forms.CharField(label='Event start time')
    end_time = forms.CharField(label='Event end time')
    additional_info = forms.CharField(label=' Is this event online anywhere? ( if yes, please provide a link ) ')


class GeneralSubmitForm (forms.Form):
    name = forms.CharField(label='Your name', max_length=150)
    email = forms.EmailField()
    event_name = forms.CharField(label=' Message: ( Please note: If you are interested in submitting an event to us, please fill out our event submit form instead. Thanks! )', max_length=400)
    

