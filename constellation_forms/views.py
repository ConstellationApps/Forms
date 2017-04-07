from django.contrib.auth.models import Group
from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from constellation_base.models import GlobalTemplateSettings
from .models import (
    Form,
    FormSubmission
)

import csv
import json


class manage_create_form(View):
    def get(self, request, form_id=None):
        ''' Returns a page that allows for the creation of new forms '''
        template_settings = GlobalTemplateSettings(allowBackground=False)
        template_settings = template_settings.settings_dict()
        groups = [(g.name, g.pk) for g in Group.objects.all()]

        form = None

        if form_id is not None:
            form = serializers.serialize(
                "json",
                Form.objects.filter(form_id=form_id)
            )

        return render(request, 'constellation_forms/create-form.html', {
            'form': form,
            'groups': groups,
            'template_settings': template_settings,
        })

    def post(self, request, form_id=None):
        ''' Creates a form '''
        form_data = json.loads(request.POST['data'])
        title = form_data['meta']['title']
        description = form_data['meta']['description']
        widgets = []
        for widget in form_data['widgets']:
            temp_widget = {}
            temp_widget['type'] = widget['type']
            if 'title' in widget:
                temp_widget['title'] = widget['title']
            if 'description' in widget:
                temp_widget['description'] = widget['description']
            if 'required' in widget and widget['required'] == 'on':
                temp_widget['required'] = True
            else:
                temp_widget['required'] = False
            if 'validator' in widget:
                temp_widget['validator'] = widget['validator']
            if 'steps' in widget:
                temp_widget['steps'] = widget['steps']
            choices = [(int(k.split('-')[1]), v) for k, v in widget.items()
                       if 'choice' in k]
            if len(choices) > 0:
                if 'other-allowed' in widget and 'other-allowed' == 'on':
                    temp_widget['other_allowed'] = True
                else:
                    temp_widget['other_allowed'] = False
                choices.sort()
                temp_widget['choices'] = [v[1] for v in choices]
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
        return HttpResponse(reverse('view_list_forms'))


class view_form(View):
    def get(self, request, form_id):
        ''' Returns a page that allows for the submittion of a created form '''
        template_settings = GlobalTemplateSettings(allowBackground=False)
        template_settings = template_settings.settings_dict()
        form = Form.objects.filter(form_id=form_id).first()

        return render(request, 'constellation_forms/submit-form.html', {
            'form': form,
            'template_settings': template_settings,
        })

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
    def get(self, request, form_submission_id):
        ''' Returns a page that displays a specific form submission instance'''
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
        print(submission_data)

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


def list_forms(request):
    ''' Returns a page that includes a list of available forms '''
    template_settings = GlobalTemplateSettings(allowBackground=False)
    template_settings = template_settings.settings_dict()
    forms_query = Form.objects.distinct('form_id')
    forms = []
    for form in forms_query:
        form.url = reverse('view_form', args=[form.form_id])
        form.edit = reverse('manage_create_form', args=[form.form_id])
        forms.append(form)

    return render(request, 'constellation_forms/list.html', {
        'template_settings': template_settings,
        'list_type': 'Forms',
        'list_items': forms,
    })


def list_submissions(request):
    ''' Returns a page that includes a list of submitted forms '''
    template_settings = GlobalTemplateSettings(allowBackground=False)
    template_settings = template_settings.settings_dict()
    submissions = FormSubmission.objects.all()
    submissions = [{
        "name": f.form.name,
        "description": f.modified,
        "state": f.state,
        "pk": f.pk,
        "url": reverse('view_form_submission', args=[f.pk]),
    } for f in submissions]

    return render(request, 'constellation_forms/list.html', {
        'template_settings': template_settings,
        'list_type': 'Form Submissions',
        'list_items': submissions,
    })


def approve_submission(request, form_submission_id):
    submission = FormSubmission.objects.get(pk=form_submission_id)
    submission.state = 2
    submission.save()
    return HttpResponseRedirect(reverse('view_list_submissions'))


def deny_submission(request, form_submission_id):
    submission = FormSubmission.objects.get(pk=form_submission_id)
    submission.state = 3
    submission.save()
    return HttpResponseRedirect(reverse('view_list_submissions'))


@csrf_exempt
def api_export(request, form_id):
    ''' Returns a serialized set of submissions for the form '''
    forms = Form.objects.filter(form_id=form_id)
    if "query" in request.GET:
        params = request.GET["query"]
    else:
        params = [f.slug for f in forms.first().elements]

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

    writer = csv.writer(response)
    writer.writerow(params)
    for form in forms:
        slug_indexes = [-1] * len(params)
        for index, element in enumerate(form.elements):
            if element in params:
                slug_indexes[params.index(element)] = index
        for submission in FormSubmission.objects.filter(form=form):
            line = []
            for index in slug_indexes:
                if index == -1:
                    line.append("")
                else:
                    line.append(submission.submission[index]['value'])
            writer.writerow(line)
    return response
