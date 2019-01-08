from django.forms import ModelForm
from core.models import LeaveReview


class LeaveReviewForm(ModelForm):
   class Meta:
       model = LeaveReview
       fields = ['reviewer', 'text', 'rating']

       