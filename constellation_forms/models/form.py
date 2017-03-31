"""
Form Database Model

In this model, the primary key is automatically generated.
(Since django does not support multi_column primary keys)

However, the unique_together attribute enforces the pair to be unique.

Ordering, the dash in front of version indicates descending.

Form elements:
    * form_id = unique id of form
    * version = specific versoin of the form_id
    * name = Name of the form (title)
    * description = Description for the form
    * elements = contains a list of dictionaries defining the elements of
        the form.  This is the converted to json, which postgres converts to
        binary data using jsonb, trading off a sligtly slower insert for
        better query performance (since the json does not need to be parsed
        every query).  This has the added advantage of making forms far
        more static once created and flattens the stucture of the database.


Element  Structure:
    [
        {
            "type": "short-answer",
            "description": "This is a test",
            "required": true,
            "validator": r"[a-z]{3}[0-9]{6}"
            ... <- More fields
        },
        ... <- More elements
    ]

Why JSONB and not the traditional relational model:
    JSON(B) storage offers the following advantages:
        * Easy to conceptualize - The relational database solution is more
          complex and makes implementation more challenging.
        * Faster - Since all data is present in a single table, pulling a form
          requires a single query
        * Static - Potential changes to other elements in the database will
          not affect previously created/submitted forms
    Typically, we would see disadvantages. Primarily, queries are more complex,
    and objects are not related.  However, since we don't need to query based
    on the contents of these fields, this does not affect the application.
"""

from django.db import models
from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ValidationError
import re


class Form(models.Model):
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

    class Meta:
        unique_together = (("form_id", "version"),)
        ordering = ("-form_id", "-version",)
        db_table = 'form'

    def __str__(self):
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
