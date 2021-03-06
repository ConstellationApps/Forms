from django.conf.urls import url

from . import views


app_name = 'constellation_forms'
urlpatterns = [
    # Management Functions
    url(r'^manage/create-form$', views.manage_create_form.as_view(),
        name="manage_create_form"),

    url(r'^manage/create-form/(?P<form_id>\d+)$',
        views.manage_create_form.as_view(),
        name="manage_create_form"),

    # View Functions
    url(r'^view/list-forms$', views.list_forms,
        name="view_list_forms"),

    url(r'^view/list-archived-forms$', views.archived_forms,
        name="view_list_archived_forms"),

    url(r'^view/form/(?P<form_id>\d+)/archive$', views.archive_form,
        name="view_archive_form"),

    url(r'^view/form/(?P<form_id>\d+)/unarchive$', views.unarchive_form,
        name="view_unarchive_form"),

    url(r'^view/list-submissions$', views.list_submissions,
        name="view_list_submissions"),

    url(r'^view/list-submissions$', views.list_submissions,
        name="view_list_submissions"),

    url(r'^view/form/(?P<form_id>\d+)$', views.view_form.as_view(),
        name="view_form"),

    url(r'^view/form/(?P<form_id>\d+)/(?P<submission_id>\d+)$',
        views.view_form.as_view(),
        name="view_form"),

    url(r'^view/submission/(?P<form_submission_id>\d+)$',
        views.view_form_submission.as_view(),
        name="view_form_submission"),

    url(r'^view/submission/(?P<form_submission_id>\d+)/request-changes$',
        views.request_changes_submission,
        name="view_request_changes_submission"),

    url(r'^view/submission/(?P<form_submission_id>\d+)/approve$',
        views.approve_submission,
        name="view_approve_submission"),

    url(r'^view/submission/(?P<form_submission_id>\d+)/provisional$',
        views.provisional_approve,
        name="view_provisional_submission"),

    url(r'^view/submission/(?P<form_submission_id>\d+)/deny$',
        views.deny_submission,
        name="view_deny_submission"),

    url(r'^api/export/(?P<form_id>\d+)$',
        views.api_export,
        name="api_export"),

    url(r'^view/dashboard$', views.view_dashboard,
        name="view_dashboard"),

    url(r'^files/log/(?P<log_id>\d+)$', views.view_log_file,
        name="view_log_file"),
]
