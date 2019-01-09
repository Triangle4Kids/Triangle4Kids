from django.forms import ModelForm
from core.models import LeaveReview, Event


class LeaveReviewForm(ModelForm):
<<<<<<< HEAD
    class Meta:
        model = LeaveReview
        fields = ['reviewer', 'text', 'rating']
=======
   class Meta:
       model = LeaveReview
       fields = [ 'text', 'rating']
>>>>>>> master

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['ages']
