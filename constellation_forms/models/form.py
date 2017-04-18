from django.db import models
from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ValidationError

from guardian.shortcuts import get_groups_with_perms

import re


class FormQuerySet(models.query.QuerySet):
    def get(self, **kwargs):
        return super().filter(**kwargs).first()


class FormManager(models.Manager.from_queryset(FormQuerySet)):
    pass


class Form(models.Model):
    """Form Database Model

    In this model, the primary key is automatically generated.  (Since
    django does not support multi_column primary keys). However, the
    unique_together attribute enforces the pair to be unique.  For
    ordering, the dash in front of version indicates descending.

    A form contains the following elements:

    * form_id = unique id of form
    * version = specific versoin of the form_id
    * name = Name of the form (title)
    * description = Description for the form
    * elements = contains a list of dictionaries defining the elements

    Elements are converted to json, which postgres converts to binary
    data using jsonb, trading off a sligtly slower insert for better
    query performance (since the json does not need to be parsed every
    query).  This has the added advantage of making forms far more
    static once created and flattens the stucture of the database.

    This deserves some explanation.  In our case JSON(B) storage offers
    the following advantages:

    Easy to conceptualize - The relational database solution is more
    complex and makes implementation more challenging.

    Faster - Since all data is present in a single table, pulling a form
    requires a single query

    Static - Potential changes to other elements in the database will
    not affect previously created/submitted forms

    Typically, we would see disadvantages. Primarily, queries are more complex,
    and objects are not related.  However, since we don"t need to query based
    on the contents of these fields, this does not affect the application.
    """

    objects = FormManager()

    element_types = [
        "boolean",
        "checkbox",
        "date",
        "dropdown",
        "instructions",
        "paragraph",
        "radio",
        "signature",
        "slider",
        "stars",
        "text",
    ]

    form_id = models.IntegerField()
    version = models.IntegerField()
    name = models.TextField()
    description = models.TextField(blank=True)
    elements = JSONField()

    @classmethod
    def can_edit(cls, user, form_id):
        """ Returns whether or not the user provided has permission to edit a
        new or existing form """
        if (form_id is None):
            return user.has_perm("constellation_forms.add_form")
        else:
            form = cls.objects.filter(form_id=form_id).first()
            return (user.has_perm("constellation_forms.form_owned_by", form) or
                    user.has_perm("constellation_forms.add_form"))

    @property
    def visible_by(self):
        """ Returns the group that has the form_visible permission """
        assigned_perms = get_groups_with_perms(self, attach_perms=True)
        if assigned_perms:
            return list(filter(lambda x: "form_visible" in assigned_perms[x],
                               assigned_perms.keys()))[0]
        else:
            return ""

    @property
    def owned_by(self):
        """ Returns the group that has the form_owner permission """
        assigned_perms = get_groups_with_perms(self, attach_perms=True)
        if assigned_perms:
            return list(filter(lambda x: "form_owned_by" in assigned_perms[x],
                               assigned_perms.keys()))[0]
        else:
            return ""

    class Meta:
        unique_together = (("form_id", "version"),)
        ordering = ("-form_id", "-version",)
        db_table = "form"
        permissions = (
            ("form_owned_by", "Form Owner"),
            ("form_visible", "Form is Visible")
        )

    def __str__(self):
        """
        <form_id>: <version> - <name>
        """
        return "{0}.{1} - {2}".format(self.form_id, self.version, self.name)

    def clean(self):
        """
        Clean function for the Form model

        This mainly focuses on ensuring the form elements are correct.
        """

        for element in self.elements:
            if "type" not in element:
                raise ValidationError("Elements are required to have a type")
            if element["type"] not in self.element_types:
                raise ValidationError("Unknown type in element")
            if "validator" in element:
                validator = element["validator"]
                try:
                    re.compile(validator)
                except:
                    raise ValidationError("Invalid validator")
