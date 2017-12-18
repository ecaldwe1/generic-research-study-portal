from django.db import models

# Create your models here.


class Participant(models.Model):
    participant_id = models.CharField(max_length=32, unique=True, blank=False, null=False)
    gmail = models.CharField(max_length=128, blank=False, null=False)
    registration_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.participant_id
