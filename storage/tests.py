from django.test import TestCase, Client
from django.contrib.auth.models import User
from storage.models import ActionType, Action


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