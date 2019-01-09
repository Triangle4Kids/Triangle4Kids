
from django.contrib import admin
from core.models import Profile, Event, Business, LeaveReview
# , Age
# Register your models here.

class EventsInLine(admin.StackedInline):
    model = Event
    list_display = ("title", "address", "link", "description", "date_of_event", "time_range", "start_date", "end_date", "city", "state", "start_time", "end_time")
    prepopulated_fields = {'slug': ('title',)}

class BusinessAdmin(admin.ModelAdmin):
    model = Business
    list_display = ("name", "address", "average_rating", "city", "state", "link")
    inlines = [EventsInLine]
    prepopulated_fields = {'slug': ('name',)}

class ReviewAdmin(admin.ModelAdmin):
    model = LeaveReview
    list_display = ("reviewer", "text", "rating")

# class AgeAdmin(admin.ModelAdmin):
#     model = Age
#     list_display = ("age_range", "AGE_RANGE_CHOICES")

admin.site.register(Business, BusinessAdmin)
admin.site.register(LeaveReview, ReviewAdmin)
# admin.site.register(Age, AgeAdmin)
