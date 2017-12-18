"""tesserae_portal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView

from portal.apps.base_portal.auth import login_request
from portal.apps.base_portal.views.custom import ProfileRedirectView, CustomLogoutView, CustomEmailLoginView

from allauth.socialaccount.views import SignupView
from allauth.socialaccount.providers.google.views import oauth2_login, oauth2_callback

from portal.apps.base_portal.views.dashboard import StaffDashboardView, ParticipantDashboardView

from portal.apps.base_portal.views.landing import LandingView

urlpatterns = [
      # url(r'^login/', login_request, name='login'),
      url(r'^$', LandingView.as_view(), name='home'),

      # url(r'^about/$', TemplateView.as_view(template_name='pages/about.html'), name='about'),

      # Django Admin, use {% url 'admin:index' %}
      url(settings.ADMIN_URL, admin.site.urls),

      # User management
      # url(r'^users/', include('portal.apps.users.urls', namespace='users')),
      # url(r'^accounts/', include('allauth.urls')),

      # Redirect from /accounts/profile/ to the home page.
      url(r'^accounts/profile/', ProfileRedirectView.as_view()),
      url(r'^accounts/logout/', CustomLogoutView.as_view()),

      url(r'^accounts/login/', CustomEmailLoginView.as_view()),

      # url(r'^accounts/google/login/', oauth2_login),
      # url(r'^accounts/google/login/callback/', oauth2_callback),

      # Include allauth urls.
      url(r'^accounts/', include('allauth.urls')),

      # Your stuff: custom urls includes go here
      url(r'^portal/', include('portal.apps.urls', namespace='portal')),
]
  # ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

