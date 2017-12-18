import smtplib
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.http.response import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView
from django.views.generic.list import ListView
from django.core.mail import EmailMessage
from django.utils.six.moves.urllib.parse import urlsplit

from portal.apps.issue_app.forms import ParticipantIssueForm, AdminUpdateIssueForm
from portal.apps.issue_app.models import Issue, IssueStatus, IssueNote
from portal.apps.participant_app.models import Participant


class IssueCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """
    Create View for Participant Users to create new Issues
    """
    model = Issue
    template_name = 'issues/create_issue.html'
    form_class = ParticipantIssueForm
    success_url = reverse_lazy('portal:issues:my_issues_list')

    def __init__(self):
        super(IssueCreate, self).__init__()
        self.object = None

    def form_valid(self, form):
        print(self.request.POST)
        self.object = form.save(commit=False)

        logged_in_participant = Participant.objects.get(gmail=self.request.user.email)

        self.object.reported_by_participant = logged_in_participant
        self.object.reported_by_user = self.request.user
        self.object.status = IssueStatus.objects.get(is_default=True)
        self.object.save()
        issue_create_notification_email(self.request, self.object)

        return HttpResponseRedirect(self.get_success_url())

    def test_func(self):
        if self.request.user.is_staff:
            return False
        else:
            return True


class MyIssueList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """
    List View to show a logged in Participant User's reported errors
    """
    model = Issue
    template_name = 'issues/view_issues_list.html'

    def get_context_data(self, **kwargs):
        context = super(MyIssueList, self).get_context_data(**kwargs)
        logged_in_participant = Participant.objects.get(gmail=self.request.user.email)
        print(logged_in_participant)
        context['issue_list'] = Issue.objects.filter(reported_by_participant=logged_in_participant).order_by('-last_updated')

        return context

    def test_func(self):
        if self.request.user.is_staff:
            return False
        else:
            return True


class AssignedIssueList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """
    List View to show issues assigned to a logged in Staff User Only
    """
    model = Issue
    template_name = 'issues/view_issues_list.html'

    def get_context_data(self, **kwargs):
        context = super(AssignedIssueList, self).get_context_data(**kwargs)
        context['issue_list'] = Issue.objects.filter(assigned_to=self.request.user).order_by('-last_updated')

        return context

    def test_func(self):
        return self.request.user.is_staff


class AllIssuesList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """
    List View to show ALL reported errors to logged in Staff Users Only
    """
    model = Issue
    template_name = 'issues/view_issues_list.html'

    def get_context_data(self, **kwargs):
        context = super(AllIssuesList, self).get_context_data(**kwargs)
        context['issue_list'] = Issue.objects.all().order_by('-last_updated')

        return context

    def test_func(self):
        return self.request.user.is_staff


class IssueDetail(LoginRequiredMixin, DetailView):
    """
    Detail View to show issue details to a logged in Participant or Staff User
    """
    model = Issue
    template_name = 'issues/issue_detail2.html'

    def get_context_data(self, **kwargs):
        context = super(IssueDetail, self).get_context_data(**kwargs)
        context['now'] = datetime.now()

        issue_notes_queryset = IssueNote.objects.filter(issue=kwargs['object'].id)
        context['note_list'] = issue_notes_queryset
        print(context)
        return context


class IssueUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Update View for Staff Users to update a reported issue
    """
    model = Issue
    template_name = 'issues/update_issue.html'
    form_class = AdminUpdateIssueForm

    def get_success_url(self):
        issue_update_notification_email(self.request, self.object)
        success_url = reverse_lazy('portal:issues:admin_assigned_issues')
        return success_url

    def form_valid(self, form):
        return super(IssueUpdate, self).form_valid(form)

    def test_func(self):
        return self.request.user.is_staff


@login_required
def add_note_view(request):
    """
    View to save the new note object to the database.
    :param request:
    :return: HttpResponse
    """
    new_note_obj = IssueNote(
        note=request.GET['note'],
        issue=Issue.objects.get(id=request.GET['issue_id']),
        author=request.user
    )
    new_note_obj.save()
    issue_update_notification_email(request, new_note_obj.issue)
    print("Created new note object: ", new_note_obj)

    return HttpResponse(200)


@login_required
def get_notes_list_view(request):
    """
    View to retrieve a list of all notes for a given issue
    :param request:
    :return: HttpResponse
    """
    issue_notes_list = IssueNote.objects.filter(issue_id=request.GET['issue_id']).order_by('-date')

    context = {'note_list': issue_notes_list}
    return render(request, '../templates/issues/issue_detail_note_list.html', context)


def issue_update_notification_email(request, issue):
    """
    Send an email to the Participant/Staff every time an issue is updated
    :param issue:
    :return:
    """
    issue_detail = build_issue_detail_url(request, issue.id)

    # Just doing this to make message a bit more readable.  Could use a template if we wanted to.
    msg_body = "This email is to inform you that the issue<br><br>" + issue.subject + "<br>" + issue.description
    msg_body += "<br><br>has been updated.<br><br>To view this issue please use the following link:<br>" + issue_detail

    # If a staff is updating issue, send the update to user. Otherwise send to staff list
    if request.user.is_staff:
        msg = EmailMessage(
            'Update: ' + issue.subject,
            msg_body,
            'tesserae@nd.edu',
            [issue.reported_by_user.email]
        )
    else:
        msg = EmailMessage(
            'Update: ' + issue.subject,
            msg_body,
            'tesserae@nd.edu',
            ['tesserae-staff-list@nd.edu']
        )

    msg.content_subtype = "html"
    msg.send()


def issue_create_notification_email(request, issue):
    """
    Send an email to Staff Users when an issue is created
    :param issue: 
    :return: 
    """
    issue_detail = build_issue_detail_url(request, issue.id)

    # Just doing this to make message a bit more readable.  Could use a template if we wanted to.
    msg_body = "Participant " + issue.reported_by_participant.participant_id +  \
               " has created a the following issue<br><br>" + issue.subject + "<br>"
    msg_body += issue.description + "<br><br>To view this issue please use the following link:<br>" + issue_detail

    msg = EmailMessage(
        'Created: ' + issue.subject,
        msg_body,
        'tesserae@nd.edu',
        ['tesserae-staff-list@nd.edu']
    )

    msg.content_subtype = "html"
    msg.send()


def build_issue_detail_url(request, id):
    """
    Builds the link that will be used to go directly to an issue detail's page
    :param id:
    :return issue_detail:
    """
    split_url = urlsplit(request.build_absolute_uri())
    issue_detail = split_url.scheme + "://" + split_url.netloc + "/portal/issues/detail/" + str(id)

    return issue_detail

