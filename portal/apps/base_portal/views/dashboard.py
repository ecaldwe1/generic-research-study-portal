from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.views.generic import TemplateView

from portal.apps.issue_app.models import Issue, IssueStatus


class ParticipantDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """
    Detail View to display status of compliance, issues, and payments to a participant
    """
    template_name = 'dashboard/participant_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(ParticipantDashboardView, self).get_context_data(**kwargs)
        my_reported_issues = Issue.objects.filter(reported_by=self.request.user).order_by('-date_reported')
        context['reported_issues'] = my_reported_issues

        context['current_month'] = datetime.today().date().strftime("%B")

        return context

    def test_func(self):
        return not self.request.user.is_staff


class StaffDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """
    Detail View to show issue details to a participant or personnel user
    """
    template_name = 'dashboard/staff_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(StaffDashboardView, self).get_context_data(**kwargs)
        my_assigned_issues = Issue.objects.filter(assigned_to=self.request.user).order_by('-date_reported')
        unassigned_issues = Issue.objects.filter(assigned_to=None).order_by('-date_reported')

        context['my_assigned_issues'] = my_assigned_issues
        context['unassigned_issues'] = unassigned_issues
        issue_status = IssueStatus.objects.all().order_by('status')
        context['status_list'] = issue_status

        context['current_month'] = datetime.today().date().strftime("%B")

        print(context)

        return context

    def test_func(self):
        return self.request.user.is_staff


@login_required
def staff_filter_issues_ajax(request):
    """
    Function based view called through Ajax to filter My Assigned Issues list based on Issue Status
    :param request: 
    :return: 
    """
    statuses = request.GET.getlist('selected_issue_statuses[]')
    status_objects = []
    for s in statuses:
        obj = IssueStatus.objects.get(status=s)
        status_objects.append(obj)

    filtered_issues = Issue.objects.filter(assigned_to=request.user,
                                           status__in=status_objects).order_by('-date_reported')
    context_dictionary = {
        'issues_list': filtered_issues

    }
    return render(request, "dashboard/issues_list.html", context_dictionary)


@login_required
def staff_filter__unassigned_issues_ajax(request):
    """
    Function based view called through Ajax to filter Unassigned Issues based on Issue Status
    :param request: 
    :return: 
    """
    statuses = request.GET.getlist('selected_issue_statuses[]')
    status_objects = []
    for s in statuses:
        obj = IssueStatus.objects.get(status=s)
        status_objects.append(obj)

    filtered_issues = Issue.objects.filter(assigned_to=None,
                                           status__in=status_objects).order_by('-date_reported')
    context_dictionary = {
        'issues_list': filtered_issues

    }
    return render(request, "dashboard/issues_list.html", context_dictionary)
