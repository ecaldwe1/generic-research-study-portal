from django.test import TestCase, Client
from django.urls import reverse

from portal.apps.users.models import User


class TestLandingView(TestCase):
    fixtures = [
        'fixtures/test/updated_users_fixture.json',
    ]

    def setUp(self):
        self.client = Client()
        self.url = reverse('home')
        user = User.objects.get(username='participant1')
        self.user = user
        user.set_password('password')
        user.save()

    # Test access to list of issues a participant has reported

    def test_participant_landing_page(self):
        self.client.login(username='participant1', password='password')
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 302)
        # self.assertEquals(len(response.context['my_compliance']), 3)

    def test_staff_landing_page(self):
        self.client.login(username='beth', password='opensesame')
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 302)

    def test_anonymous_landing_page(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
