from django.forms import ModelForm
from core.models import LeaveReview
from django import forms


class LeaveReviewForm(ModelForm):
   class Meta:
       model = LeaveReview
       fields = ['reviewer', 'text', 'rating']


class EventForm(forms.Form):
    title = forms.CharField(label='Event/Class/Camp Name', max_length=255)
    cost = 
    category = 
    description = forms.TextField(label='description')
    date = forms.DateField(, required=False)
    time = forms.TimeField(, required=False)
    age =
    link = forms.URLField(, required=False)
    phone =
    email = forms.EmailField(, required=False)
    address = 
    photo = 