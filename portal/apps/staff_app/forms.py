from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from portal.apps.staff_app.models import Staff


class StaffForm(forms.ModelForm):
    """
    This form is used for superusers to add new staff members
    """

    def __init__(self, *args, **kwargs):
        super(StaffForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Add Staff Member', css_class='btn-primary pull-right'))

    class Meta:
        model = Staff
        fields = [
            'name',
            'gmail',
            'affiliation',
        ]


