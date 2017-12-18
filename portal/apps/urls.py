from django.conf.urls import include, url

from portal.apps.base_portal.views.dashboard import StaffDashboardView, ParticipantDashboardView, \
    staff_filter__unassigned_issues_ajax, staff_filter_issues_ajax

urlpatterns = [
    url(r'^staff-dashboard/filter-issues', staff_filter_issues_ajax,
        name='staff_filter_issues'),
    url(r'^staff-dashboard/filter-unassigned-issues', staff_filter__unassigned_issues_ajax,
        name='staff_filter__unassigned_issues'),

    url(r'^staff/', include('portal.apps.staff_app.urls', namespace='staff')),
    url(r'^issues/', include('portal.apps.issue_app.urls', namespace='issues')),
    url(r'^staff-dashboard', StaffDashboardView.as_view(), name='staff_dashboard'),
    url(r'^dashboard', ParticipantDashboardView.as_view(), name='participant_dashboard'),

]
