from django.forms import ModelForm
from core.models import LeaveReview, Event


class LeaveReviewForm(ModelForm):
    class Meta:
        model = LeaveReview
        fields = ['reviewer', 'text', 'rating']

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['ages']
