"""
Form Submission Database Model

A form submission object is a specific, submitted/drafted instance of a form.

Attributes:
    * form - the specific form instance that the submission references
    * state - the state field specifies the current status for the submission.
        may be one of ["draft", "submitted", "approved", or "denied"]
    * modified - last date modified
    * owner - user submitting the form
    * submission - serialized submission information
        + Array indexes MUST match the form elements.
"""

from .form import Form
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ValidationError
from django.db import models
import re


class FormSubmission(models.Model):
    states = (
        (0, "draft"),
        (1, "submitted"),
        (2, "approved"),
        (3, "denied"),
    )

    form = models.ForeignKey(Form)
    state = models.IntegerField(choices=states)
    modified = models.DateField()
    owner = models.ForeignKey(User, blank=True, null=True)
    submission = JSONField()

    class Meta:
        db_table = 'form_submission'

    def __str__(self):
        return "{0}: {1} {2} {3}".format(self.form, self.modified, self.owner,
                                         self.state)

    def clean(self):
        if len(self.form.elements) != len(self.submission):
            raise ValidationError("Number of submission elements must match.")

        for index, element in enumerate(self.form.elements):
            sub_element = self.submission[index]
            if ("required" in element and element["required"]) and (
                    sub_element is None and self.state > 0):
                raise ValidationError("Required element blank.")
            if "validator" in element and sub_element is not None:
                regex = re.compile(element["validator"])
                if not regex.match(sub_element):
                    raise ValidationError("Validator did not match entry.")
            if "choices" in element and sub_element:
                if ("other_choice" not in element or
                        not element["other_choice"]):
                    if element["type"] == "choice":
                        if sub_element not in element["choices"]:
                            raise ValidationError("Invalid choice.")
                    elif element["type"] == "multichoice":
                        for c in sub_element:
                            if c not in element["choices"]:
                                raise ValidationError("Invalid choice.")
