from django.test import TestCase, Client
from django.urls import reverse

from portal.apps.users.models import User


class ParticipantDashboardView(TestCase):
    fixtures = [
        'fixtures/test/updated_users_fixture.json',
        'fixtures/test/issue_app_fixture.json',
        'fixtures/test/compliance_app_fixture.json',
    ]

    def setUp(self):
        self.client = Client()
        self.url = reverse('portal:participant_dashboard')
        user = User.objects.get(username='participant1')
        self.user = user
        user.set_password('password')
        user.save()

    # Test access to list of issues a participant has reported

    def test_participant_dashboard_participant_user(self):
        self.client.login(username='participant1', password='password')
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        # self.assertEquals(len(response.context['my_compliance']), 3)

    def test_survey_compliance_list_staff_user(self):
        self.client.login(username='beth', password='opensesame')
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 302)
