from django.db import models


# Staff member model
class Staff(models.Model):
    name = models.CharField(max_length=128, blank=False, null=False)
    gmail = models.CharField(max_length=128, blank=False, null=False)
    affiliation = models.CharField(max_length=256, blank=True, null=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name + ' ' + self.gmail
