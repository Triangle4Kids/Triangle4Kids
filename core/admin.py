
from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from core.models import Profile, Event, Business, LeaveReview, MushroomSpot
# Register your models here.

class ReviewAdmin(admin.ModelAdmin):
    model = MushroomSpot
    list_display = ("geom", "address")

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

admin.site.register(Business, BusinessAdmin)
admin.site.register(LeaveReview, ReviewAdmin)
admin.site.register(MushroomSpot, LeafletGeoAdmin)
