"""
Adds all individual files to models.

Necesary for django to find and use the models correctly.
"""

from .form import Form  # noqa: 401
from .formSubmission import FormSubmission  # noqa: 401
from .validator import Validator  # noqa: 401
from .apiKey import ApiKey # noqa: 401
