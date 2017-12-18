from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from portal.apps.issue_app.models import Issue, IssueNote


class ParticipantIssueForm(forms.ModelForm):
    """
    This form is used for participants to create a new issue.
    """

    def __init__(self, *args, **kwargs):
        super(ParticipantIssueForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Report Issue', css_class='btn-primary pull-right'))

    class Meta:
        model = Issue
        fields = [
            'category',
            'subject',
            'description',
            'preferred_contact_method',
        ]


class AdminUpdateIssueForm(forms.ModelForm):
    """
    This form is used for Admins to update an issue
    """
    def __init__(self, *args, **kwargs):
        super(AdminUpdateIssueForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Update Issue', css_class='btn-primary pull-right'))
        self.fields['reported_by_participant'].disabled = True

    subject = forms.CharField(label='Subject', disabled=True)
    description = forms.CharField(label="Description", widget=forms.Textarea, disabled=True)

    class Meta:
        model = Issue
        fields = [
            'subject',
            'description',
            'category',
            'assigned_to',
            'status',
            'reported_by_participant',
        ]


class IssueNoteForm(forms.ModelForm):
    """
    This form is used to add a note to a reported issue. 
    Administrators and Participants use the same form.
    """

    def __init__(self, *args, **kwargs):
        super(IssueNoteForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Add Note', css_class='btn-primary pull-right'))

    class Meta:
        model = IssueNote
        fields = [
            'note'
        ]
