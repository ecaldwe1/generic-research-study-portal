from django.conf.urls import url

from portal.apps.issue_app.views import IssueCreate, MyIssueList, AllIssuesList, IssueUpdate, IssueDetail, \
    add_note_view, get_notes_list_view, AssignedIssueList

urlpatterns = [
    url(r'^create$', IssueCreate.as_view(), name='new_issue'),
    url(r'^my-issues$', MyIssueList.as_view(), name='my_issues_list'),
    url(r'^list$', AllIssuesList.as_view(), name='all_issues_list'),
    url(r'^my-assigned-issues$', AssignedIssueList.as_view(), name='admin_assigned_issues'),
    url(r'^update/(?P<pk>\d+)$', IssueUpdate.as_view(), name='admin_issues_update'),
    url(r'^detail/(?P<pk>\d+)$', IssueDetail.as_view(), name='issue_details'),
    url(r'^submit-note$', add_note_view, name='submit_note'),
    url(r'^get-note-list$', get_notes_list_view, name='get_note_list')

]
