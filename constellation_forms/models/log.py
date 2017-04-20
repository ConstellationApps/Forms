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
    * private - display to non-owners?
    * message - log entry
    * mtype - type of log entry
      * 1 - user message (default)
      * 2 - system action
      * 3 - form status change
      * 4 - attached file
    * file - attached file entry
    """

    owner = models.ForeignKey(User, blank=True, null=True)
    submission = models.ForeignKey(FormSubmission)
    timestamp = models.DateTimeField(auto_now_add=True)
    private = models.BooleanField(default=False)
    message = models.TextField(blank=True)
    mtype = models.IntegerField(default=1)
    file = models.FileField(upload_to='log_files/')

    class Meta:
        db_table = "form_log"
        ordering = ("-timestamp",)
