from django.conf.urls import url

from . import views


urlpatterns = [
    # Management Functions
    url(r'^manage/create-form$', views.manage_create_form.as_view(),
        name="manage_create_form"),

    # View Functions
    url(r'^view/list-forms$', views.list_forms,
        name="view_list_forms"),

    url(r'^view/list-submissions$', views.list_submissions,
        name="view_list_submissions"),

    url(r'^view/form/(?P<form_id>\d+)$', views.view_form.as_view(),
        name="view_form"),
]
