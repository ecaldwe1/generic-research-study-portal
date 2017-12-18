from django.contrib import admin

# Register your models here.
from portal.apps.staff_app.models import Staff


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('name', 'gmail', 'affiliation', 'date_added')
