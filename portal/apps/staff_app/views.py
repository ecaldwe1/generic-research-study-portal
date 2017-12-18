from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from portal.apps.staff_app.forms import StaffForm
from portal.apps.staff_app.models import Staff


class StaffCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """
    Create View for new Issues
    """
    model = Staff
    template_name = 'staff/create_staff.html'
    form_class = StaffForm
    success_url = reverse_lazy('portal:staff_dashboard')

    def __init__(self):
        super(StaffCreate, self).__init__()
        self.object = None

    def form_valid(self, form):
        print(self.request.POST)
        self.object = form.save(commit=True)

        return HttpResponseRedirect(self.get_success_url())

    def test_func(self):
        if self.request.user.is_staff and self.request.user.is_superuser:
            return True
        else:
            return False
