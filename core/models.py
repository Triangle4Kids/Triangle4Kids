from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import django_filters

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
 
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Business(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    average_rating = models.FloatField(default="0")
    link = models.URLField(null=True, blank=True)
    slug = models.SlugField(unique=True, max_length=255)

    class Meta:
        verbose_name_plural = "Businesses"

    def __str__(self):
        return self.name

# class AgeRange(models.Model):

#     PRE_K = 1
#     ELEMENTARY = 2
#     MIDDLE = 3
#     HIGH = 4
    

#     event = models.ForeignKey("Event", on_delete=models.CASCADE, related_name="age_ranges")
#     age = models.ForeignKey("Age", on_delete=models.CASCADE, related_name="age_ranges")
#     # range = models.IntegerField(choices=AGE_RANGE_CHOICES, blank=True, null=True)

class Event(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name="events")
    ages = models.ManyToManyField("Age", related_name="events")
    title = models.CharField(max_length=255)
    link = models.URLField(null=True, blank=True)
    description = models.TextField()
    slug = models.SlugField(unique=True, max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    start_time = models.CharField(max_length=255)
    end_time = models.CharField(max_length=255)
    favorite = models.ManyToManyField(User, related_name='favorite', blank=True)
    ages = models.ManyToManyField("Age", related_name="events")
# For django-filters categories
    # pre_k = models.BooleanField(default=False)
    # elementary = models.BooleanField(default=False)
    # middle = models.BooleanField(default=False)
    # high = models.BooleanField(default=False)
    # half_day = models.BooleanField(default=False)
    # full_day = models.BooleanField(default=False)
    # academic = models.BooleanField(default=False)
    # arts_and_crafts = models.BooleanField(default=False)
    # games = models.BooleanField(default=False)
    # language = models.BooleanField(default=False)
    # nature_outdoor = models.BooleanField(default=False)
    # performance = models.BooleanField(default=False)
    # stem = models.BooleanField(default=False)
    # other = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Age(models.Model):
    PRE_K = 'PRE-K'
    ELEMENTARY = 'ELEMENTARY'
    MIDDLE = 'MIDDLE'
    HIGH = 'HIGH'

    AGE_RANGE_CHOICES = (
        (PRE_K, 'Pre-K'),
        (ELEMENTARY, 'Elementary'),
        (MIDDLE, 'Middle'),
        (HIGH, 'High'),
    )
    age_range = models.CharField(
        max_length=12,
        choices=AGE_RANGE_CHOICES,
        blank=True, null=True
    )

    def __str__(self):
        return self.age_range
    
    

# class EventFilter(django_filters.FilterSet):
#     class Meta:
#         verbose_name_plural = "Events"
#         model = Event
#         fields = {
#             'age': ['pre_k', 'elementary', 'middle', 'high'],
#             'city': ['carrboro', 'Chapel_Hill', 'Durham', 'Morrisville',             'Raleigh', 'RTP'],
#             'type': ['class', 'camp', 'full_day', 'half_day'],
#             'theme': ['academic', 'arts_and_crafts', 'games', 'language',             'nature_outdoor', 'performance', 'stem', 'other'],
#         }


class LeaveReview(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name="reviews")
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=500, blank=False)
    rating = models.IntegerField(default="0") 

    class Meta:
        verbose_name_plural = "Reviews"

    def __str__(self):
        return self.title

