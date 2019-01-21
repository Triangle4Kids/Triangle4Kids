from django.contrib import admin
from core.models import Profile, Event, Business, LeaveReview, \
    BusinessLatLong, EventLatLong

# Register your models here.


class EventLatLongInLine(admin.StackedInline):
    model = EventLatLong
    list_display = ("site_name", "relevance", "latitude", "longitude")


class EventsInLine(admin.StackedInline):
    model = Event
    list_display = ("title", "link", "description", "address", "city", "state",
                    "start_date", "end_date", "start_time", "end_time")
    prepopulated_fields = {'slug': ('title', )}


class EventAdmin(admin.ModelAdmin):
    model = Event
    list_display = ("title", "link", "description", "address", "city", "state",
                    "start_date", "end_date", "start_time", "end_time")
    inlines = [EventLatLongInLine]
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


admin.site.register(Event, EventAdmin)
admin.site.register(Business, BusinessAdmin)
admin.site.register(LeaveReview, ReviewAdmin)
