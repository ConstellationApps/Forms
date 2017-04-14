"""
API Key Database Model

Attributes:
    * user - owner of api_key
    * key - text key
"""

from django.contrib.auth.models import User
from django.db import models


class ApiKey(models.Model):
    # only allow 1 key per user
    user = models.OneToOneField(User)
    key = models.TextField()

    def __str__(self):
        return "{0} ({1})".format(self.user, self.key)
