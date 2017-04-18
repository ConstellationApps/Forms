from .formSubmission import FormSubmission
from django.contrib.auth.models import User
from django.db import models


class Log(models.Model):
    """
    Form Submission Log Database Model

    Attributes:

    * owner - user submitting the message
    * submission - form submission associated
    * timestamp - time of submission entry

    """

    owner = models.ForeignKey(User, blank=True, null=True)
    submission = models.ForeignKey(FormSubmission)
    timestamp = models.DateTimeField(auto_now_add=True)
    private = models.BooleanField(default=False)
    message = models.TextField(blank=True)
    file = models.FileField(upload_to='log_files/')

    class Meta:
        db_table = "form_log"
        ordering = ("-timestamp",)
