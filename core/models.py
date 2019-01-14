from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from multiselectfield import MultiSelectField
from django.core.validators import MinValueValidator, MaxValueValidator
from phone_field import PhoneField


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
    phone = PhoneField(blank=True, help_text='Contact phone number')
    average_rating = models.FloatField(default="0")
    link = models.URLField(null=True, blank=True)
    slug = models.SlugField(unique=True, max_length=255)

    class Meta:
        verbose_name_plural = "Businesses"

    def __str__(self):
        return self.name


EVENT_TYPE = (
    ('half_day', 'Half-Day'),
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

AGE_RANGE = (
    ('pre_k', 'Pre-K'),
    ('elementary', 'Elementary'),
    ('middle', 'Middle'),
    ('high', 'High'),
)

CLASS_CAMP = (
    ('class', 'Class'),
    ('camp', 'Camp'),
    ('homeschool', 'Homeschool'),
)

CITIES = (
    ('raleigh', 'Raleigh'),
    ('durham', 'Durham'),
    ('cary', 'Cary'),
    ('chapel_hill', 'Chapel Hill'),
    ('morrisville', 'Morrisville'),
    ('rtp', 'RTP'),
    ('carrboro', 'Carrboro'),
)


class Event(models.Model):
    type_choice = MultiSelectField(choices=EVENT_TYPE, null=True, blank=False)
    age_choice = models.CharField(
        max_length=20, null=True, blank=False, choices=AGE_RANGE)
    class_camp_choice = models.CharField(
        max_length=10, null=True, blank=False, choices=CLASS_CAMP)
    cities_choice = models.CharField(
        max_length=30, null=True, blank=False, choices=CITIES)
    date_created = models.DateTimeField(auto_now_add=True)
    business = models.ForeignKey(
        Business, on_delete=models.CASCADE, related_name="events")
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
    favorite = models.ManyToManyField(
        User, related_name='favorite', blank=True)

    class Meta:
        verbose_name_plural = "Events"

    def __str__(self):
        return self.title


class LeaveReview(models.Model):
    business = models.ForeignKey(
        Business, on_delete=models.CASCADE, related_name="reviews")
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=500, blank=False)
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1),
                    MaxValueValidator(5)])

    class Meta:
        verbose_name_plural = "Reviews"

    def __str__(self):
        return self.title


#class Location
# event location
#
# business location
# search box would be a map filter
# JS would take fields from search box to construct the map
# have a city that is "anywhere" that is show all
# how to get info in/out from database from JS...will need to do query against the db
# events in the next month
# js class map_builder
# create rest api that allows to get event data / manipulating objects in db
# only object that has access to python models is rest api
# "separation of concerns"
#
#
#
#
##
#
#
#
