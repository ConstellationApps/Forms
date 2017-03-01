from django.conf.urls import url

from . import views


urlpatterns = [
    # Management Functions
    url(r'^manage/create-form$', views.manage_create_form,
        name="manage_create_form"),
]
