from django.conf.urls import url

from portal.apps.staff_app.views import StaffCreate

urlpatterns = [
    url(r'^new-staff', StaffCreate.as_view(), name='new_staff'),

]