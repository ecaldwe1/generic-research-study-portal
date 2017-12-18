from django.contrib import admin

# Register your models here.
from portal.apps.issue_app.models import IssueCategory, IssueStatus, Issue, IssueNote, IssueContactMethod

admin.site.register(IssueCategory)
admin.site.register(IssueStatus)
admin.site.register(IssueContactMethod)
admin.site.register(Issue)
admin.site.register(IssueNote)
