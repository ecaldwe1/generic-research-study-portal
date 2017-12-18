"""
ReferebcesL http://django-allauth.readthedocs.io/en/latest/advanced.html?highlight=DefaultAccountAdapter

"""


from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter

class CustomAccountAdapter(DefaultAccountAdapter):

    # def get_login_redirect_url(self, request):
    #     path = "/accounts/{username}/"
    #     return path.format(username=request.user.username)

    def is_open_for_signup(self, request):
        return True

