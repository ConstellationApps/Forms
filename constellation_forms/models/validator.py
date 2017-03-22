from django.core.exceptions import ValidationError
from django.db import models
import re


class Validator(models.Model):
    """
    Validator Database Model

    Attributes:
        * name - name of validator
        * regex - regex for validator
    """
    name = models.TextField()
    regex = models.TextField()

    class Meta:
        db_table = 'validators'

    def __str__(self):
        return "{0} ({1})".format(self.name, self.regex)

    def clean(self):
        try:
            re.compile(self.regex)
        except:
            raise ValidationError("Invalid validator")
