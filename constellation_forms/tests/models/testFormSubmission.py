from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone
from ...models import Form
from ...models import FormSubmission


class FormSubmissionModelTest(TestCase):
    def setUp(self):
        form = [
            {
                "type": "text",
                "name": "NetID",
                "description": "xxx000000",
                "validator": r"[a-z]{3}[0-9]{6}",
                "required": True
            },
        ]
        form = Form(form_id=1, version=1, name="TestForm", description="",
                    elements=form)
        form.full_clean()
        form.save()

        form2 = [
            {
                "type": "choice",
                "name": "pizza",
                "description": "toppings",
                "choices": ["cheese", "pepperoni"]
            },
        ]
        form = Form(form_id=2, version=1, name="TestForm", description="",
                    elements=form2)
        form.full_clean()
        form.save()

        form2[0]["other_choice"] = True
        form = Form(form_id=4, version=1, name="TestForm", description="",
                    elements=form2)
        form.full_clean()
        form.save()

        form2[0]["type"] = "multichoice"
        form2[0]["other_choice"] = False
        form = Form(form_id=3, version=1, name="TestForm", description="",
                    elements=form2)
        form.full_clean()
        form.save()

    def test_good_submission(self):
        form = Form.objects.get(form_id=1, version=1)
        submission = ["dbo130030"]
        form_sub = FormSubmission(form=form, state=0, modified=timezone.now(),
                                  submission=submission)
        form_sub.full_clean()

    def test_invalid_submission_validator(self):
        form = Form.objects.get(form_id=1, version=1)
        submission = ["notanetid"]
        form_sub = FormSubmission(form=form, state=0, modified=timezone.now(),
                                  submission=submission)
        self.assertRaises(ValidationError, form_sub.full_clean)
        form_sub.save()
        form_sub.delete()

    def test_valid_submission_choice(self):
        form = Form.objects.get(form_id=2, version=1)
        submission = ["pepperoni"]
        form_sub = FormSubmission(form=form, state=0, modified=timezone.now(),
                                  submission=submission)
        form_sub.full_clean()
        form_sub.save()
        form_sub.delete()

    def test_invalid_submission_choice(self):
        form = Form.objects.get(form_id=2, version=1)
        submission = ["pineapple"]
        form_sub = FormSubmission(form=form, state=0, modified=timezone.now(),
                                  submission=submission)
        self.assertRaises(ValidationError, form_sub.full_clean)
        form_sub.save()
        form_sub.delete()

    def test_valid_submission_choices(self):
        form = Form.objects.get(form_id=3, version=1)
        submission = [["pepperoni", "cheese"]]
        form_sub = FormSubmission(form=form, state=0, modified=timezone.now(),
                                  submission=submission)
        form_sub.full_clean()
        form_sub.save()
        form_sub.delete()

    def test_invalid_submission_choices(self):
        form = Form.objects.get(form_id=3, version=1)
        submission = [["pepperoni", "pineapple"]]
        form_sub = FormSubmission(form=form, state=0, modified=timezone.now(),
                                  submission=submission)
        self.assertRaises(ValidationError, form_sub.full_clean)
        form_sub.save()
        form_sub.delete()

    def test_valid_submission_other_choice(self):
        form = Form.objects.get(form_id=4, version=1)
        submission = ["pineapple"]
        form_sub = FormSubmission(form=form, state=0, modified=timezone.now(),
                                  submission=submission)
        form_sub.full_clean()
        form_sub.save()
        form_sub.delete()

    def test_invalid_submission_required(self):
        form = Form.objects.get(form_id=1, version=1)
        submission = [None]
        form_sub = FormSubmission(form=form, state=1, modified=timezone.now(),
                                  submission=submission)
        self.assertRaises(ValidationError, form_sub.full_clean)
        form_sub.save()
        form_sub.delete()

    def test_str(self):
        form = Form.objects.get(form_id=1, version=1)
        submission = ["dbo130030"]
        form_sub = FormSubmission(form=form, state=0, modified=timezone.now(),
                                  submission=submission)
        str(form_sub)

    def test_too_few_elements(self):
        form = Form.objects.get(form_id=1, version=1)
        submission = []
        form_sub = FormSubmission(form=form, state=0, modified=timezone.now(),
                                  submission=submission)
        self.assertRaises(ValidationError, form_sub.full_clean)

    def tearDown(self):
        Form.objects.get(form_id=1, version=1).delete()
        Form.objects.get(form_id=2, version=1).delete()
        Form.objects.get(form_id=3, version=1).delete()
