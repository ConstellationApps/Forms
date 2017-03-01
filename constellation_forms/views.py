from django.contrib.auth.models import Group
from django.shortcuts import render

from constellation_base.models import GlobalTemplateSettings


def manage_create_form(request):
    ''' Returns a page that allows for the creation of new forms '''
    template_settings_object = GlobalTemplateSettings(allowBackground=False)
    template_settings = template_settings_object.settings_dict()
    groups = [(g.name, g.pk) for g in Group.objects.all()]

    return render(request, 'constellation_forms/create-form.html', {
        'groups': groups,
        'template_settings': template_settings,
    })
