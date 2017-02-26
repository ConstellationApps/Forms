from django.core.exceptions import ValidationError
from django.test import TestCase
from ...models import Form


class FormModelTest(TestCase):
    def test_good_form(self):
        form = [
            {
                "type": "text",
                "name": "NetID",
                "description": "xxx000000",
                "validator": r"[a-z]{3}[0-9]{6}",
            },
        ]
        form = Form(form_id=1, version=1, name="TestForm", description="",
                    elements=form)
        form.full_clean()
        form.save()
        form.delete()

    def test_invalid_form(self):
        form = [
            {
                "type": "NOTAREALFORMELEMENT",
                "name": "NetID",
                "description": "xxx000000",
                "validator": r"[a-z]{3}[0-9]{6}",
            },
        ]
        form = Form(form_id=1, version=1, name="TestForm", description="",
                    elements=form)
        self.assertRaises(ValidationError, form.full_clean)

    def test_no_type(self):
        form = [
            {
                "name": "NetID",
                "description": "xxx000000",
                "validator": r"[a-z]{3}[0-9]{6}",
            },
        ]
        form = Form(form_id=1, version=1, name="TestForm", description="",
                    elements=form)
        self.assertRaises(ValidationError, form.full_clean)

    def test_invalid_validator(self):
        form = [
            {
                "type": "text",
                "name": "NetID",
                "description": "xxx000000",
                "validator": r"[",
            },
        ]
        form = Form(form_id=1, version=1, name="TestForm", description="",
                    elements=form)
        self.assertRaises(ValidationError, form.full_clean)

    def test_string(self):
        form = [
            {
                "type": "text",
                "name": "NetID",
                "description": "xxx000000",
                "validator": r"]",
            },
        ]
        form = Form(form_id=1, version=1, name="TestForm", description="",
                    elements=form)
        str(form)
