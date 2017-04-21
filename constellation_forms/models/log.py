from .formSubmission import FormSubmission
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify


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
    file = models.FileField(upload_to='private/constellation_forms/log_files/')

    class Meta:
        db_table = "form_log"
        ordering = ("timestamp",)

    @property
    def extension(self):
        return self.file.name.split(".")[-1]

    @property
    def content_type(self):
        if self.extension == "pdf":
            return "application/pdf"
        if self.extension == "txt":
            return "text/plain"
        if self.extension == "png":
            return "image/png"
        if self.extension == "jpeg" or self.extension == "jpg":
            return "image/jpeg"
        if self.extension == "gif":
            return "image/gif"
        return "application/force-download"

    @property
    def file_name(self):
        return slugify("{0}_{1}_{2}".format(self.submission.form.name, self.pk,
                                            self.owner.username)) + "." + \
                self.extension
