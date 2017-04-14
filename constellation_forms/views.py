from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import (
    Group,
    User
)
from django.conf import settings
from django.core import serializers
from django.db import transaction
from django.shortcuts import redirect, render
from django.http import (
    HttpResponse,
    HttpResponseForbidden,
    HttpResponseRedirect
)
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse

from guardian.decorators import (
    permission_required,
    permission_required_or_403,
)

from guardian.shortcuts import assign_perm, get_objects_for_user

from constellation_base.models import GlobalTemplateSettings
from .models import (
    Form,
    FormSubmission
)

from .util import api_key_required

import csv
import json


class manage_create_form(View):
    @method_decorator(login_required)
    def get(self, request, form_id=None):
        """ Returns a page that allows for the creation of new forms """
        # We can"t use a method decorator here, because we need to check
        # different conditions depending on whether or not a form_id is given
        # Someone with add_form can add a new form or edit an existing form,
        # and form owners can edit existing forms that they own
        if not Form.can_edit(request.user, form_id):
            return redirect("%s?next=%s" % (
                settings.LOGIN_URL, request.path))

        template_settings = GlobalTemplateSettings(allowBackground=False)
        template_settings = template_settings.settings_dict()
        groups = [(g.name, g.pk) for g in Group.objects.all()]

        form = None
        form_data = None

        if form_id is not None:
            form = Form.objects.filter(form_id=form_id).first()
            form_data = serializers.serialize(
                "json", Form.objects.filter(form_id=form_id),
            )

        return render(request, "constellation_forms/create-form.html", {
            "form": form,
            "form_data": form_data,
            "visible_groups": groups,
            "template_settings": template_settings,
        })

    @method_decorator(login_required)
    def post(self, request, form_id=None):
        """ Creates a form """
        if not Form.can_edit(request.user, form_id):
            return HttpResponseForbidden()
        form_data = json.loads(request.POST["data"])
        title = form_data["meta"]["title"]
        description = form_data["meta"]["description"]
        widgets = []
        with transaction.atomic():
            for widget in form_data["widgets"]:
                temp_widget = {}
                temp_widget["type"] = widget["type"]
                if "title" in widget:
                    temp_widget["title"] = widget["title"]
                if "description" in widget:
                    temp_widget["description"] = widget["description"]
                if "required" in widget and widget["required"] == "on":
                    temp_widget["required"] = True
                else:
                    temp_widget["required"] = False
                if "validator" in widget:
                    temp_widget["validator"] = widget["validator"]
                if "steps" in widget:
                    temp_widget["steps"] = widget["steps"]
                choices = [(int(k.split("-")[1]), v) for k, v in widget.items()
                           if "choice" in k]
                if len(choices) > 0:
                    if "other-allowed" in widget and "other-allowed" == "on":
                        temp_widget["other_allowed"] = True
                    else:
                        temp_widget["other_allowed"] = False
                    choices.sort()
                    temp_widget["choices"] = [v[1] for v in choices]
                widgets.append(temp_widget)

            # This is not safe, but it will work for now...
            if not form_id:
                if Form.objects.all().count() > 0:
                    last_form = Form.objects.all().order_by("-form_id").first()
                    form_id = last_form.form_id + 1
                else:
                    form_id = 1
                version = 1
            else:
                current_form = Form.objects.filter(form_id=form_id).first()
                version = current_form.version + 1

            new_form = Form(
                version=version,
                form_id=form_id,
                name=title,
                description=description,
                elements=widgets,
            )
            new_form.full_clean()
            new_form.save()

            # Add permissions
            visible_group = Group.objects.get(
                name=form_data["options"]["visible"])
            assign_perm("form_visible", visible_group, new_form)
            owner_group = Group.objects.get(name=form_data["options"]["owner"])
            assign_perm("form_owned_by", owner_group, new_form)
            assign_perm("form_visible", owner_group, new_form)

        return HttpResponse(reverse("view_list_forms"))


class view_form(View):
    @method_decorator(login_required)
    @method_decorator(permission_required('constellation_forms.form_visible',
                                          (Form, 'form_id', 'form_id')))
    def get(self, request, form_id):
        ''' Returns a page that allows for the submittion of a created form '''
        template_settings = GlobalTemplateSettings(allowBackground=False)
        template_settings = template_settings.settings_dict()
        form = Form.objects.filter(form_id=form_id).first()

        return render(request, 'constellation_forms/submit-form.html', {
            'form': form,
            'template_settings': template_settings,
        })

    @method_decorator(permission_required_or_403(
        'constellation_forms.form_visible',
        (Form, 'form_id', 'form_id')))
    def post(self, request, form_id):
        ''' Creates a form '''
        form = Form.objects.filter(form_id=form_id).first()
        form_data = json.loads(request.POST['data'])['widgets']
        user = request.user
        state = 1  # submitted

        new_submission = FormSubmission(
            form=form,
            owner=user,
            state=state,
            submission=form_data,
            modified=timezone.now()
        )
        new_submission.full_clean()
        new_submission.save()
        return HttpResponse(reverse('view_list_submissions'))


class view_form_submission(View):
    @method_decorator(login_required)
    def get(self, request, form_submission_id):
        ''' Returns a page that displays a specific form submission instance'''
        if not FormSubmission.can_view(request.user, form_submission_id):
            return redirect("%s?next=%s" % (
                settings.LOGIN_URL, request.path))
        template_settings = GlobalTemplateSettings(allowBackground=False)
        template_settings = template_settings.settings_dict()
        submission = FormSubmission.objects.get(pk=form_submission_id)
        submission_data = []
        for index, value in enumerate(submission.submission):
            element = {}
            for tag in ('title', 'description', 'type', 'steps'):
                if tag not in submission.form.elements[index]:
                    continue
                element[tag] = submission.form.elements[index][tag]
            element['value'] = value
            submission_data.append(element)

        return render(request, 'constellation_forms/view-submission.html', {
            'template_settings': template_settings,
            'name': submission.form.name,
            'description': submission.form.description,
            'state': submission.state,
            'id': form_submission_id,
            'widgets': submission_data,
            'form_id': submission.form.form_id,
            'version': submission.form.version,
        })


@login_required
def list_forms(request):
    ''' Returns a page that includes a list of available forms '''
    template_settings = GlobalTemplateSettings(allowBackground=False)
    template_settings = template_settings.settings_dict()
    owned_forms = get_objects_for_user(
        request.user,
        "constellation_forms.form_owned_by",
        Form).distinct("form_id")
    available_forms = get_objects_for_user(
        request.user,
        "constellation_forms.form_visible",
        Form).distinct("form_id")
    forms = [{"name": "Owned Forms", "list_items": []},
             {"name": "Available Forms", "list_items": []}]

    for form in owned_forms:
        form.url = reverse('view_form', args=[form.form_id])
        form.edit = reverse('manage_create_form', args=[form.form_id])
        forms[0]["list_items"].append(form)

    for form in available_forms:
        if form not in owned_forms:
            form.url = reverse('view_form', args=[form.form_id])
            form.edit = reverse('manage_create_form', args=[form.form_id])
            forms[1]["list_items"].append(form)

    return render(request, 'constellation_forms/list.html', {
        'template_settings': template_settings,
        'list_type': 'Forms',
        'lists': forms,
    })


@login_required
def list_submissions(request):
    ''' Returns a page that includes a list of submitted forms '''
    template_settings = GlobalTemplateSettings(allowBackground=False)
    template_settings = template_settings.settings_dict()
    submissions = FormSubmission.objects.all()

    staff = request.user.has_perm("constellation_forms.form_create")
    filter_query = {}
    print(request.GET)
    if "username" in request.GET and len(request.GET['username']) > 0:
        r_username = request.GET['username']
        if User.objects.filter(username=r_username).exists():
            temp_user = User.objects.get(username=r_username)
            filter_query["owner"] = temp_user
    if "form" in request.GET and len(request.GET['form']) > 0:
        r_form = request.GET['form']
        if Form.objects.filter(form_id=r_form).exists():
            temp_form = list(Form.objects.filter(form_id=r_form))
            filter_query["form__in"] = temp_form

    if staff and len(filter_query) > 0:
        submissions = FormSubmission.objects.filter(**filter_query)
    else:
        submissions = FormSubmission.objects.all()

    forms = [{"name": "Pending Submissions", "list_items": []},
             {"name": "Incoming Submissions", "list_items": []},
             {"name": "Done Submissions", "list_items": []}]

    forms[0]["list_items"] = [{
        "name": f.form.name,
        "description": f.modified,
        "state": f.state,
        "pk": f.pk,
        "url": reverse('view_form_submission', args=[f.pk]),
    } for f in submissions if request.user == f.owner and f.state == 1]

    forms[1]["list_items"] = [{
        "name": f.form.name,
        "owner": f.owner.username,
        "description": f.modified,
        "state": f.state,
        "pk": f.pk,
        "url": reverse('view_form_submission', args=[f.pk]),
    } for f in submissions
        if (request.user.has_perm("constellation_forms.form_owned_by", f.form)
            and (f.state == 1))]

    forms[2]["list_items"] = [{
        "name": f.form.name,
        "owner": f.owner.username,
        "description": f.modified,
        "state": f.state,
        "pk": f.pk,
        "url": reverse('view_form_submission', args=[f.pk]),
    } for f in submissions
        if (request.user.has_perm("constellation_forms.form_owned_by", f.form)
            or request.user == f.owner) and (f.state == 2 or f.state == 3)]

    return render(request, 'constellation_forms/list.html', {
        'template_settings': template_settings,
        'list_type': 'Form Submissions',
        'lists': forms,
        'forms': Form.objects.all().distinct('form_id'),
    })


@login_required
def approve_submission(request, form_submission_id):
    if not FormSubmission.can_approve(request.user, form_submission_id):
        return HttpResponseForbidden()
    submission = FormSubmission.objects.get(pk=form_submission_id)
    submission.state = 2
    submission.save()
    return HttpResponseRedirect(reverse('view_list_submissions'))


@login_required
def deny_submission(request, form_submission_id):
    if not FormSubmission.can_approve(request.user, form_submission_id):
        return HttpResponseForbidden()
    submission = FormSubmission.objects.get(pk=form_submission_id)
    submission.state = 3
    submission.save()
    return HttpResponseRedirect(reverse('view_list_submissions'))


@csrf_exempt
@api_key_required()
def api_export(request, form_id):
    ''' Returns a serialized set of submissions for the form '''
    forms = Form.objects.filter(form_id=form_id)
    if "query" in request.GET:
        params = request.GET["query"]
    else:
        first_form_elements = forms.first().elements
        if "slug" in first_form_elements[0]:
            params = [f['slug'] for f in first_form_elements]
        else:
            params = [f['title'] for f in first_form_elements]

    response = HttpResponse(content_type='text')

    writer = csv.writer(response)
    writer.writerow(params)
    for form in forms:
        slug_indexes = [-1] * len(params)
        for index, element in enumerate(form.elements):
            if "slug" in element and element['slug'] in params:
                slug_indexes[params.index(element['slug'])] = index
            elif "title" in element and element['title'] in params:
                slug_indexes[params.index(element['title'])] = index
        for submission in FormSubmission.objects.filter(form=form):
            line = []
            for index in slug_indexes:
                if index == -1:
                    line.append("")
                else:
                    line.append(submission.submission[index])
            writer.writerow(line)
    return response

# -----------------------------------------------------------------------------
# Dashboard
# -----------------------------------------------------------------------------


@login_required
def view_dashboard(request):
    '''Return a card that will appear on the main dashboard'''

    return render(request, 'constellation_forms/dashboard.html')
