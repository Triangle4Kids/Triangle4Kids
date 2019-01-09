from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from multiselectfield import MultiSelectField


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


EVENT_TYPE = (('half_day', 'Half-Day'),
              ('full_day', 'Full-Day'),
              ('academic', 'Academic'),
              ('arts_crafts', 'Arts & Crafts'),
              ('athletics', 'Athletics'),
              ('games', 'Games'),
              ('language', 'Language'),
              ('nature_outdoor', 'Nature/Outdoor'),
              ('performance', 'Performance'),
              ('stem', 'STEM'),
              ('other', 'Other'),
              )

AGE_RANGE = (('pre_k', 'Pre-K'),
             ('elementary', 'Elementary'),
             ('middle', 'Middle'),
             ('high', 'High'),
             )

CLASS_CAMP = (('class', 'Class'),
              ('camp', 'Camp'),
              )

CITIES = (('raleigh', 'Raleigh'),
          ('durham', 'Durham'),
          ('cary', 'Cary'),
          ('chapel_hill', 'Chapel Hill'),
          )

class Event(models.Model):
    type_choice = MultiSelectField(choices=EVENT_TYPE, null=True, blank=False)
    age_choice = models.CharField(max_length=20, null=True, blank=False, choices=AGE_RANGE)
    class_camp_choice = models.CharField(max_length=10, null=True, blank=False, choices=CLASS_CAMP)
    cities_choice = models.CharField(max_length=30, null=True, blank=False, choices=CITIES)
    date_created = models.DateTimeField(auto_now_add=True)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name="events")
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

    class Meta:
        verbose_name_plural = "Events"

    def __str__(self):
        return self.title


class LeaveReview(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name="reviews")
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=500, blank=False)
    rating = models.IntegerField(default="0") 

    class Meta:
        verbose_name_plural = "Reviews"

    def __str__(self):
        return self.title
