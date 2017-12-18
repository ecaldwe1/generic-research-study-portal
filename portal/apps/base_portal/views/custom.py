from django.views.generic import RedirectView
from django.contrib.auth import logout
from django.urls import reverse

from allauth.account.views import LogoutView

from allauth.socialaccount.views import ConnectionsView

class ProfileRedirectView(RedirectView):
    """
    Redirect from 'login' where it takes you to '/accounts/profile/'.
    It redirects to 'root' page or 'next' if any is filled out.
    """
    def get_redirect_url(self, *args, **kwargs):

        print(self.request.user.email)

        url = "portal:participant_dashboard"
        if self.request.user.is_staff:
            url = "portal:staff_dashboard"

        print("===========================")
        print("IN THE PROFILE REDIRECT VIEW")
        print(self.request.user)
        print(url)
        print("===========================")

        return self.request.GET.get('next', reverse(url))

class CustomLogoutView(LogoutView):
    """
    Custom view that allows changing of the template provided by 'allauth' to use 'our' templates.
    NOTE: View does not add or remove any functionality!
    """
    template_name = "allauth/logout.html"

class CustomEmailLoginView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return "/accounts/google/login/?action=reauthenticate"