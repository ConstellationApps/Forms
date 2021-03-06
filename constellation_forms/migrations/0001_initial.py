# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-15 00:56
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Form',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('form_id', models.IntegerField()),
                ('version', models.IntegerField()),
                ('name', models.TextField()),
                ('description', models.TextField(blank=True)),
                ('elements', django.contrib.postgres.fields.jsonb.JSONField()),
            ],
            options={
                'ordering': ('-version',),
                'db_table': 'form',
            },
        ),
        migrations.CreateModel(
            name='FormSubmission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.IntegerField(choices=[(0, 'draft'), (1, 'submitted'), (2, 'approved'), (3, 'denied')])),
                ('modified', models.DateField()),
                ('submission', django.contrib.postgres.fields.jsonb.JSONField()),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='constellation_forms.Form')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'form_submission',
            },
        ),
        migrations.CreateModel(
            name='Validator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('regex', models.TextField()),
            ],
            options={
                'db_table': 'validators',
            },
        ),
        migrations.AlterUniqueTogether(
            name='form',
            unique_together=set([('form_id', 'version')]),
        ),
    ]
