from django.forms import ModelForm
from core.models import LeaveReview, Event
# from uni_form.helper import FormHelper
from crispy_forms.helper import FormHelper


class LeaveReviewForm(ModelForm):
    class Meta:
        model = LeaveReview
        fields = [
            'title', 'event', 'rating', 'text',
        ]


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = [
            'title', 'business', 'link', 'description', 'start_date', 'end_date', 'start_time', 'end_time', 'image', 'type_choice', 'age_choice', 'class_camp_choice', 'address', 'city', 'state',
        ]
