# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-05 03:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('constellation_forms', '0008_form_archived'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formsubmission',
            name='state',
            field=models.IntegerField(choices=[(0, 'draft'), (1, 'submitted'), (2, 'changes requested'), (3, 'approved'), (4, 'denied')]),
        ),
    ]