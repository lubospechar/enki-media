from django.contrib.auth.models import User
from django.contrib.admin.sites import AdminSite
from django.test import TestCase, Client, RequestFactory
from django.contrib.auth import get_user_model
from storage.models import UploadedFile
from storage.admin import UploadedFileAdmin
from django.core.files.uploadedfile import SimpleUploadedFile
import os

User = get_user_model()


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
        expected_fields = ('download_url', "author", "user", "uploaded_at", "is_public", 'qr_code_preview')
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
