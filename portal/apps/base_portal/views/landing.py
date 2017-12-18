from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.base import TemplateView


class LandingView(TemplateView):
    """
    Template view for the landing page
    """
    template_name = 'landing-page.html'

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_anonymous:
            url = "portal:participant_dashboard"
            if self.request.user.is_staff:
                url = "portal:staff_dashboard"
            return HttpResponseRedirect(reverse(url))
        else:
            context = self.get_context_data(**kwargs)
            return self.render_to_response(context)
