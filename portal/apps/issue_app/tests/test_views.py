from django.test import TestCase, Client
from django.urls import reverse

from portal.apps.users.models import User


class TestIssueCreate(TestCase):
    fixtures = [
        'fixtures/test/updated_users_fixture.json',
        'fixtures/test/issue_app_fixture.json'
    ]

    def setUp(self):
        self.client = Client()
        self.url = reverse('portal:issues:new_issue')
        user = User.objects.get(username='participant1')
        self.user = user
        user.set_password('password')
        user.save()

    # Test that all logged in users can access the new issue page

    def test_issue_create_page_participant_user(self):
        self.client.login(username='participant1', password='password')
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)

    def test_issue_create_page_staff_user(self):
        self.client.login(username='beth', password='opensesame')
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 302)

    def test_issue_create_page_no_user(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 302)

    # Test that all logged in users can successfully create a new issue

    def test_valid_issue_create_participant_user(self):
        self.client.login(username='participant1', password='password')
        url = reverse('portal:issues:new_issue')
        response = self.client.post(url, {
            'submit': ['Report Issue'],
            'category': ['1'],
            'subject': ['Another New Issue'],
            'description': ["I'm creating one now!"],
            'preferred_contact_method': ['1']
        })
        self.assertRedirects(response, reverse('portal:issues:my_issues_list'),
                             status_code=302, target_status_code=200)


class TestMyIssueListView(TestCase):
    fixtures = [
        'fixtures/test/updated_users_fixture.json',
        'fixtures/test/issue_app_fixture.json',
    ]

    def setUp(self):
        self.client = Client()
        self.url = reverse('portal:issues:my_issues_list')
        user = User.objects.get(username='participant1')
        self.user = user
        user.set_password('password')
        user.save()

    # Test access to list of issues a participant has reported

    def test_my_issue_list_participant_user(self):
        self.client.login(username='participant1', password='password')
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.context['issue_list']), 7)

    def test_my_issue_list_staff_user(self):
        self.client.login(username='beth', password='opensesame')
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 302)

    # def test_my_issue_list_no_user(self):
    #     response = self.client.get(self.url)
    #     redirect_url = reverse('login') + '?next=' + self.url
    #     self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)


class TestAssignedIssueListView(TestCase):
    fixtures = [
        'fixtures/test/updated_users_fixture.json',
        'fixtures/test/issue_app_fixture.json',
    ]

    def setUp(self):
        self.client = Client()
        self.url = reverse('portal:issues:admin_assigned_issues')
        user = User.objects.get(username='participant1')
        self.user = user
        user.set_password('password')
        user.save()

    # Test access to my assigned issues page

    def test_assigned_issue_list_participant_user(self):
        self.client.login(username='participant1', password='password')
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 302)

    def test_assigned_issue_list_staff_user(self):
        self.client.login(username='beth', password='opensesame')
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.context['issue_list']), 5)

    # def test_that_302_is_thrown_for_no_user(self):
    #     response = self.client.get(self.url)
    #     redirect_url = reverse('login') + '?next=' + self.url
    #     self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)


class TestAllIssueListView(TestCase):
    fixtures = [
        'fixtures/test/updated_users_fixture.json',
        'fixtures/test/issue_app_fixture.json',
    ]

    def setUp(self):
        self.client = Client()
        self.url = reverse('portal:issues:all_issues_list')
        user = User.objects.get(username='participant1')
        self.user = user
        user.set_password('password')
        user.save()

    # Test access to list of all issues

    def test_all_issue_list_staff_user(self):
        self.client.login(username='beth', password='opensesame')
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.context['issue_list']), 9)

    def test_all_issue_list_participant_user(self):
        self.client.login(username='participant1', password='password')
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 302)

    # def test_all_issue_list_no_user(self):
    #     response = self.client.get(self.url)
    #     redirect_url = reverse('login') + '?next=' + self.url
    #     self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)


class TestMyIssueDetailView(TestCase):
    fixtures = [
        'fixtures/test/updated_users_fixture.json',
        'fixtures/test/issue_app_fixture.json',
    ]

    def setUp(self):
        self.client = Client()
        self.url = reverse('portal:issues:issue_details', kwargs={'pk': 2})
        user = User.objects.get(username='participant1')
        self.user = user
        user.set_password('password')
        user.save()

    # Test access to my issue detail page

    def test_my_issue_detail_staff_user(self):
        self.client.login(username='beth', password='opensesame')
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)

    def test_my_issue_detail_participant_user(self):
        self.client.login(username='participant1', password='password')
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)

    # def test_my_issue_detail_no_user(self):
    #     response = self.client.get(self.url)
    #     redirect_url = reverse('login') + '?next=' + self.url
    #     self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)


class TestIssueUpdateView(TestCase):
    fixtures = [
        'fixtures/test/updated_users_fixture.json',
        'fixtures/test/issue_app_fixture.json',
    ]

    def setUp(self):
        self.client = Client()
        self.url = reverse('portal:issues:admin_issues_update', kwargs={'pk': 2})
        user = User.objects.get(username='participant1')
        self.user = user
        user.set_password('password')
        user.save()

    # Test access to update issue page

    def test_update_issue_page_staff_user(self):
        self.client.login(username='beth', password='opensesame')
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)

    def test_update_issue_page_participant_user(self):
        self.client.login(username='participant1', password='password')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    # def test_update_issue_page_no_user(self):
    #     response = self.client.get(self.url)
    #     redirect_url = reverse('login') + '?next=' + self.url
    #     self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    # Test that issue can be updated by staff user

    def test_valid_issue_update_staff_user(self):
        self.client.login(username='beth', password='opensesame')
        url = reverse('portal:issues:admin_issues_update', kwargs={'pk': 2})
        response = self.client.post(url, {
            'status': ['1'],
            'assigned_to': ['2'],
            'category': ['1'],
            'submit': ['Update Issue']
        })
        self.assertRedirects(response, reverse('portal:issues:admin_assigned_issues'),
                             status_code=302, target_status_code=200)


class TestAddNoteView(TestCase):
    fixtures = [
        'fixtures/test/updated_users_fixture.json',
        'fixtures/test/issue_app_fixture.json',
    ]

    def setUp(self):
        self.client = Client()
        self.url = reverse('portal:issues:submit_note')
        user = User.objects.get(username='participant1')
        self.user = user
        user.set_password('password')
        user.save()

    def test_add_note_staff_user(self):
        self.client.login(username='beth', password='opensesame')
        response = self.client.get(self.url, {'note': "Yay another new note!", 'issue_id': 2})
        self.assertEquals(response.status_code, 200)

    def test_add_note_participant_user(self):
        self.client.login(username='participant1', password='password')
        response = self.client.get(self.url, {'note': "Yay a new note!", 'issue_id': 2})
        self.assertEquals(response.status_code, 200)

    # def test_add_note_no_user(self):
    #     response = self.client.get(self.url)
    #     redirect_url = reverse('login') + '?next=' + self.url
    #     self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)


class TestGetNotesListView(TestCase):
    fixtures = [
        'fixtures/test/updated_users_fixture.json',
        'fixtures/test/issue_app_fixture.json',
    ]

    def setUp(self):
        self.client = Client()
        self.url = reverse('portal:issues:get_note_list')
        user = User.objects.get(username='participant1')
        self.user = user
        user.set_password('password')
        user.save()

    # Test access to notes list

    def test_get_notes_list_staff_user(self):
        self.client.login(username='participant1', password='password')
        response = self.client.get(self.url, {'issue_id': 2})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.context['note_list']), 2)

    def test_get_notes_list_participant_user(self):
        self.client.login(username='participant1', password='password')
        response = self.client.get(self.url, {'issue_id': 2})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.context['note_list']), 2)

    # def test_get_notes_list_no_user(self):
    #     response = self.client.get(self.url, {'issue_id': 2})
    #     self.assertEquals(response.status_code, 302)

