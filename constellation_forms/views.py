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
        form_data = json.dumps(request.POST['data'])
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
        try:
            new_form.full_clean()
            new_form.save()
        except:
            # invalid form
            pass


def list_forms(request):
        ''' Returns a page that includes a list of available forms '''
        template_settings = GlobalTemplateSettings(allowBackground=False)
        template_settings = template_settings.settings_dict()
        groups = [(g.name, g.pk) for g in Group.objects.all()]
        forms = Form.objects.all()

        return render(request, 'constellation_forms/list-forms.html', {
            'groups': groups,
            'template_settings': template_settings,
            'forms': forms
        })


def list_submissions(request):
        ''' Returns a page that includes a list of submitted forms '''
        template_settings = GlobalTemplateSettings(allowBackground=False)
        template_settings = template_settings.settings_dict()
        groups = [(g.name, g.pk) for g in Group.objects.all()]
        submissions = FormSubmission.objects.all()

        return render(request, 'constellation_forms/list-submissions.html', {
            'groups': groups,
            'template_settings': template_settings,
            'submissions': submissions
        })
