from django.contrib.auth.models import User, Group, Permission
from django.test import TestCase, RequestFactory
from guardian.shortcuts import assign_perm
from ... import views
from ...models import Form


class PermissionsTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.group = Group.objects.create(name="Test Group")
        self.group.save()
        self.user = User.objects.create_user(
            username="user",
            email="user@example.com",
            password="pass")
        self.user.save()
        self.permission = Permission.objects.get(
            codename="add_form")
        self.form = Form.objects.create(form_id=1,
                                        version=1,
                                        name="TestForm",
                                        description="",
                                        elements={})

    def tearDown(self):
        self.user.delete()
        self.group.delete()
        self.form.delete()

    # Test editing new forms
    def test_form_create_get_unauthorized(self):
        request = self.factory.get("/forms/manage/create-form")
        request.user = self.user
        response = views.manage_create_form.as_view()(request)
        self.assertEqual(response.status_code, 302)

    def test_form_create_post_unauthorized(self):
        request = self.factory.post("/forms/manage/create-form")
        request.user = self.user
        response = views.manage_create_form.as_view()(request)
        self.assertEqual(response.status_code, 403)

    def test_form_create_get_authorized(self):
        request = self.factory.get("/forms/manage/create-form")
        self.user.user_permissions.add(self.permission)
        request.user = self.user
        response = views.manage_create_form.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_form_create_post_authorized(self):
        request = self.factory.post("/forms/manage/create-form")
        self.user.user_permissions.add(self.permission)
        request.user = self.user
        # We just want to pass the permission check
        self.assertRaises(KeyError,
                          views.manage_create_form.as_view(),
                          request)

    # Test editing existing forms
    def test_edit_get_unauthorized(self):
        request = self.factory.get("/forms/manage/create-form/1")
        request.user = self.user
        response = views.manage_create_form.as_view()(request)
        self.assertEqual(response.status_code, 302)

    def test_edit_post_unauthorized(self):
        request = self.factory.post("/forms/manage/create-form/1")
        request.user = self.user
        response = views.manage_create_form.as_view()(request)
        self.assertEqual(response.status_code, 403)

    def test_edit_get_authorized(self):
        request = self.factory.get("/forms/manage/create-form/1")
        self.user.user_permissions.add(self.permission)
        request.user = self.user
        response = views.manage_create_form.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_edit_post_authorized(self):
        request = self.factory.post("/forms/manage/create-form/1")
        self.user.user_permissions.add(self.permission)
        request.user = self.user
        # We just want to pass the permission check
        self.assertRaises(KeyError,
                          views.manage_create_form.as_view(),
                          request)

    def test_edit_get_in_group(self):
        request = self.factory.get("/forms/manage/create-form/1")
        self.user.groups.add(self.group)
        assign_perm("constellation_forms.form_owned_by", self.group, self.form)
        assign_perm("constellation_forms.form_visible", self.group, self.form)
        request.user = self.user
        response = views.manage_create_form.as_view()(request, form_id=1)
        self.assertEqual(response.status_code, 200)

    def test_edit_post_in_group(self):
        request = self.factory.post("/forms/manage/create-form/1")
        self.user.groups.add(self.group)
        assign_perm("constellation_forms.form_owned_by", self.group, self.form)
        assign_perm("constellation_forms.form_visible", self.group, self.form)
        request.user = self.user
        # We just want to pass the permission check
        self.assertRaises(
            KeyError,
            views.manage_create_form.as_view(),
            request,
            form_id=1)

    def test_view_form_unauthorized(self):
        request = self.factory.get("/forms/view/form/1")
        request.user = self.user
        response = views.view_form.as_view()(request, form_id=1)
        self.assertEqual(response.status_code, 302)

    def test_view_post_unauthorized(self):
        request = self.factory.post("/forms/view/form/1")
        request.user = self.user
        response = views.view_form.as_view()(request, form_id=1)
        self.assertEqual(response.status_code, 403)

    def test_view_form_in_group(self):
        request = self.factory.get("/forms/view/form/1")
        self.user.groups.add(self.group)
        request.user = self.user
        assign_perm("constellation_forms.form_visible", self.group, self.form)
        response = views.view_form.as_view()(request, form_id=1)
        self.assertEqual(response.status_code, 200)

    def test_view_post_in_group(self):
        request = self.factory.post("/forms/view/form/1")
        self.user.groups.add(self.group)
        request.user = self.user
        assign_perm("constellation_forms.form_visible", self.group, self.form)
        self.assertRaises(
            KeyError,
            views.view_form.as_view(),
            request,
            form_id=1)
