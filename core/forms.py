from django.forms import ModelForm
from django import forms
from core.models import LeaveReview, CITIES

class LeaveReviewForm(ModelForm):
    class Meta:
        model = LeaveReview
        fields = ['text', 'rating']


class CViewerForm(forms.Form):

    status = forms.ChoiceField(
        choices=CITIES, label="Raleigh", initial='', widget=forms.Select(), required=True
    )
