from django.contrib import admin
from core.models import Profile, Event, Business, LeaveReview, BusinessLatLong

# Register your models here.


class EventsInLine(admin.StackedInline):
    model = Event
    list_display = ("title", "address", "link", "description", "date_of_event",
                    "time_range", "start_date", "end_date", "city", "state",
                    "start_time", "end_time")
    prepopulated_fields = {'slug': ('title', )}


class BizLatLongInline(admin.StackedInline):
    model = BusinessLatLong
    list_display = ("location_name", "relevance", "latitude", "longitude")


class BusinessAdmin(admin.ModelAdmin):
    model = Business
    list_display = ("name", "address", "average_rating", "city", "state",
                    "link")
    inlines = [BizLatLongInline, EventsInLine]
    prepopulated_fields = {'slug': ('name', )}


class ReviewAdmin(admin.ModelAdmin):
    model = LeaveReview
    list_display = ("reviewer", "text", "rating")


admin.site.register(Business, BusinessAdmin)
admin.site.register(LeaveReview, ReviewAdmin)
