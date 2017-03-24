from django.contrib.auth.models import Group
from django.shortcuts import render
from django.views import View
from constellation_base.models import GlobalTemplateSettings
from .models import (
    Form,
    FormSubmission
)

import json


class manage_create_form(View):
    def get(self, request):
        ''' Returns a page that allows for the creation of new forms '''
        template_settings = GlobalTemplateSettings(allowBackground=False)
        template_settings = template_settings.settings_dict()
        groups = [(g.name, g.pk) for g in Group.objects.all()]

        return render(request, 'constellation_forms/create-form.html', {
            'groups': groups,
            'template_settings': template_settings,
        })

    def post(self, request):
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
        if Form.objects.all().count() > 0:
            form_id = Form.objects.all().order_by("-form_id")[0] + 1
        else:
            form_id = 1

        new_form = Form(
            version=1,
            form_id=form_id,
            name=title,
            description=description,
            elements=widgets,
        )
        new_form.full_clean()
        new_form.save()


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


def list_forms(request):
        ''' Returns a page that includes a list of available forms '''
        template_settings = GlobalTemplateSettings(allowBackground=False)
        template_settings = template_settings.settings_dict()
        forms = Form.objects.all()

        return render(request, 'constellation_forms/list.html', {
            'template_settings': template_settings,
            'list_type': 'Forms',
            'list_items': forms
        })


def list_submissions(request):
        ''' Returns a page that includes a list of submitted forms '''
        template_settings = GlobalTemplateSettings(allowBackground=False)
        template_settings = template_settings.settings_dict()
        submissions = FormSubmission.objects.all()

        return render(request, 'constellation_forms/list.html', {
            'template_settings': template_settings,
            'list_type': 'Form Submissions',
            'list_items': submissions
        })
