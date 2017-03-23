from django.conf.urls import url

from . import views


urlpatterns = [
    # Management Functions
    url(r'^manage/create-form$', views.manage_create_form.as_view(),
        name="manage_create_form"),
]
