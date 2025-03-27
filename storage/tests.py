from django.contrib.auth.models import User
from storage.models import ActionType, Action
from django.contrib.admin.sites import AdminSite
from django.test import TestCase, Client, RequestFactory
from django.contrib.auth import get_user_model
from storage.models import UploadedFile
from storage.admin import UploadedFileAdmin
from django.core.files.uploadedfile import SimpleUploadedFile
import os

User = get_user_model()


class ActionTypeModelTests(TestCase):
    def test_create_action_type(self):
        """Test creating an ActionType"""
        action_type = ActionType.objects.create(name="Conference")
        self.assertEqual(action_type.name, "Conference")
        self.assertEqual(str(action_type), "Conference")

    def test_str_method(self):
        """Test the __str__ method of ActionType"""
        action_type = ActionType.objects.create(name="Seminar")
        self.assertEqual(str(action_type), "Seminar")

class ActionModelTests(TestCase):
    def test_create_action(self):
        """Test creating an Action linked to ActionType"""
        action_type = ActionType.objects.create(name="Seminar")
        action = Action.objects.create(type=action_type, name="Django Workshop")

        self.assertEqual(action.name, "Django Workshop")
        self.assertEqual(action.type, action_type)
        self.assertEqual(str(action), "Seminar: Django Workshop")

    def test_str_method(self):
        """Test the __str__ method of Action"""
        action_type = ActionType.objects.create(name="Project")
        action = Action.objects.create(type=action_type, name="New App Development")
        self.assertEqual(str(action), "Project: New App Development")

    def test_delete_action_type_cascade(self):
        """Test that deleting an ActionType deletes associated Actions"""
        action_type = ActionType.objects.create(name="Project")
        action = Action.objects.create(type=action_type, name="New App Development")

        action_type.delete()

        self.assertFalse(Action.objects.filter(name="New App Development").exists())


class AdminAccessTests(TestCase):
    def setUp(self):
        """Create a test user and client"""
        self.client = Client()
        self.admin_user = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="password"
        )
        self.client.login(username="admin", password="password")

        self.action_type = ActionType.objects.create(name="Seminar")
        self.action = Action.objects.create(type=self.action_type, name="Django Workshop")

    def test_admin_action_type_listed(self):
        """Test that ActionType is listed in admin"""
        response = self.client.get("/admin/storage/actiontype/")
        self.assertEqual(response.status_code, 200)

    def test_admin_action_listed(self):
        """Test that Action is listed in admin"""
        response = self.client.get("/admin/storage/action/")
        self.assertEqual(response.status_code, 200)

    def test_admin_action_type_change_page(self):
        """Test that ActionType edit page loads"""
        response = self.client.get(f"/admin/storage/actiontype/{self.action_type.id}/change/")
        self.assertEqual(response.status_code, 200)

    def test_admin_action_change_page(self):
        """Test that Action edit page loads"""
        response = self.client.get(f"/admin/storage/action/{self.action.id}/change/")
        self.assertEqual(response.status_code, 200)

class UploadedFileAdminTests(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.factory = RequestFactory()

        self.admin_user = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="password"
        )
        self.regular_user = User.objects.create_user(
            username="user", email="user@example.com", password="password"
        )

        self.uploaded_file_admin = UploadedFileAdmin(UploadedFile, self.site)

        self.file1 = UploadedFile.objects.create(
            user=self.regular_user,
            author="John Doe",
            stored_file=SimpleUploadedFile("testfile.txt", b"content"),
            is_public=True
        )

    def tearDown(self):
        """Remove all test files after each test"""
        for uploaded_file in UploadedFile.objects.all():
            file_path = uploaded_file.stored_file.path
            if os.path.exists(file_path):
                os.remove(file_path)

    def test_admin_list_display(self):
        """Test that admin list display is set correctly"""
        expected_fields = ("id", "stored_file", "author", "user", "uploaded_at", "is_public", "qr_code_preview")
        self.assertEqual(self.uploaded_file_admin.list_display, expected_fields)

    def test_admin_queryset_superuser(self):
        """Test that superuser sees all files in the admin panel"""
        request = self.factory.get("/admin/")
        request.user = self.admin_user
        queryset = self.uploaded_file_admin.get_queryset(request)
        self.assertIn(self.file1, queryset)

    def test_admin_queryset_regular_user(self):
        """Test that a regular user sees only their own files"""
        request = self.factory.get("/admin/")
        request.user = self.regular_user
        queryset = self.uploaded_file_admin.get_queryset(request)
        self.assertIn(self.file1, queryset)

        new_file = UploadedFile.objects.create(
            user=self.admin_user,
            author="Admin Author",
            stored_file=SimpleUploadedFile("adminfile.txt", b"content"),
            is_public=False
        )
        self.assertNotIn(new_file, queryset)

    def test_admin_has_change_permission(self):
        """Test that regular users can only change their own files"""
        request = self.factory.get("/admin/")
        request.user = self.regular_user
        self.assertTrue(self.uploaded_file_admin.has_change_permission(request, self.file1))

        new_file = UploadedFile.objects.create(
            user=self.admin_user,
            author="Admin Author",
            stored_file=SimpleUploadedFile("adminfile.txt", b"content"),
            is_public=False
        )
        self.assertFalse(self.uploaded_file_admin.has_change_permission(request, new_file))

    def test_admin_has_delete_permission(self):
        """Test that regular users can only delete their own files"""
        request = self.factory.get("/admin/")
        request.user = self.regular_user
        self.assertTrue(self.uploaded_file_admin.has_delete_permission(request, self.file1))

        new_file = UploadedFile.objects.create(
            user=self.admin_user,
            author="Admin Author",
            stored_file=SimpleUploadedFile("adminfile.txt", b"content"),
            is_public=False
        )
        self.assertFalse(self.uploaded_file_admin.has_delete_permission(request, new_file))
