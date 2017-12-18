from django.db import models

from portal.apps.participant_app.models import Participant
from portal.apps.users.models import User
# Create your models here.


# Issue Category model
class IssueCategory(models.Model):
    name = models.CharField(max_length=512)

    def __str__(self):
        return self.name


# Issue Status model
class IssueStatus(models.Model):
    status = models.CharField(max_length=128)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.status


# Contact Method model
class IssueContactMethod(models.Model):
    contact_method = models.CharField(max_length=128)

    def __str__(self):
        return self.contact_method


# Issue model
class Issue(models.Model):
    OPEN = 'Open'
    CLOSED = 'Closed'
    ISSUE_STATUS_CHOICES = (
        (OPEN, 'Open'),
        (CLOSED, 'Closed')
    )
    subject = models.CharField(max_length=1024, blank=False, null=False)
    description = models.TextField(default="", blank=False, null=False)
    reported_by_participant = models.ForeignKey(Participant, related_name='reporting_participant', blank=False, null=False)
    reported_by_user = models.ForeignKey(User, related_name='reporting_user', blank=False, null=False)
    date_reported = models.DateTimeField(auto_now_add=True)
    status = models.ForeignKey('IssueStatus', related_name='issue_status', blank=False, null=False)
    last_updated = models.DateTimeField(auto_now=True)
    category = models.ForeignKey('IssueCategory', related_name='issue_category', blank=False, null=False)
    assigned_to = models.ForeignKey(User, related_name='assigned_admin', limit_choices_to={'is_staff': True},
                                    blank=True, null=True)
    preferred_contact_method = models.ForeignKey('IssueContactMethod', related_name='issue_contact_method', blank=False,
                                                 null=False)

    def __str__(self):
        return '%s - %s' % (self.subject, self.date_reported)

    def get_reportedby_name(self):
        return self.reported_by_participant.participant_id


# Issue Note model - reporting user and admin can add notes to an issue
class IssueNote(models.Model):
    note = models.TextField(default="", blank=True, null=True)
    author = models.ForeignKey(User, related_name="note_author", blank=False, null=False)
    date = models.DateTimeField(auto_now=True)
    issue = models.ForeignKey('Issue', related_name='note_issue', blank=False, null=False)

    def __str__(self):
        return '%i -- %s' % (self.issue.id, self.note)
