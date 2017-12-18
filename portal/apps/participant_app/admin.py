from django.contrib import admin

# Register your models here.
from portal.apps.participant_app.models import Participant


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('participant_id', 'gmail', 'registration_date')
