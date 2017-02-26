from django.test import TestCase
from django.core.exceptions import ValidationError
from ...models import Validator


class ValidatorModelTest(TestCase):
    def test_creation(self):
        validator = Validator(name="name", regex=r"[a-zA-Z]+")
        validator.save()

    def test_invalid(self):
        validator = Validator(name="name", regex=r"(")
        self.assertRaises(ValidationError, validator.full_clean)

    def test_string(self):
        validator = Validator(name="name", regex=r"[a-zA-Z]+")
        str(validator)
